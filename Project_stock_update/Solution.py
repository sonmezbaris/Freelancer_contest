"""
Odoo’daki stock.warehouse.orderpoint (min/max stok kuralı) modelini genişlet.

Son 6 ay satışlarını (stock.move) çek

Her ürün için zaman serisi

Transformer tabanlı zaman serisi tahmin modeli ile satış tahmini

Bmin_qty ve max_qty değerlerini güncelle

"""


from odoo import models, api
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import torch
from torch import nn

# Basit Transformer modeli
class TimeSeriesTransformer(nn.Module):
    def __init__(self, input_dim=1, d_model=64, nhead=4, num_layers=2, output_dim=1):
        super(TimeSeriesTransformer, self).__init__()
        self.input_linear = nn.Linear(input_dim, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.output_linear = nn.Linear(d_model, output_dim)

    def forward(self, src):
        src = self.input_linear(src)
        out = self.transformer_encoder(src)
        out = self.output_linear(out[-1])
        return out

class SmartReplenishment(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.model
    def _forecast_sales_transformer(self, series, n_steps=30):
        # Transformeri çalıştırmak için veri hazırla
        series = np.array(series[-n_steps:], dtype=np.float32)
        src = torch.tensor(series).unsqueeze(1).unsqueeze(1)  # [seq_len, batch=1, features=1]

        model = TimeSeriesTransformer()
        model.eval()
        with torch.no_grad():
            forecast = model(src)
        return float(forecast.item())

    @api.model
    def update_min_max_forecast(self):
        date_from = datetime.today() - timedelta(days=180)  # son 6 ay
        moves = self.env['stock.move'].search([
            ('state', '=', 'done'),
            ('picking_type_id.code', '=', 'outgoing'),
            ('date', '>=', date_from)
        ])

        data = []
        for move in moves:
            data.append({
                'date': move.date,
                'product_id': move.product_id.id,
                'qty': move.product_uom_qty
            })

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])

        forecast_results = {}
        for product_id in df['product_id'].unique():
            series = df[df['product_id']==product_id]['qty'].values
            if len(series) < 30:
                continue
            forecast_qty = self._forecast_sales_transformer(series)
            forecast_results[product_id] = forecast_qty

        # Orderpoint güncelle
        for product_id, forecast_qty in forecast_results.items():
            orderpoint = self.env['stock.warehouse.orderpoint'].search([
                ('product_id','=',product_id)
            ], limit=1)
            if orderpoint:
                max_qty = forecast_qty
                min_qty = forecast_qty / 2  # + safety stock eklenebilir
                orderpoint.write({
                    'product_max_qty': max_qty,
                    'product_min_qty': min_qty
                })
