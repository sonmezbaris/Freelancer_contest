<odoo>
    <data noupdate="1">
        <record id="ir_cron_transformer_smart_replenishment" model="ir.cron">
            <field name="name">Transformer Smart Replenishment Update</field>
            <field name="model_id" ref="stock.model_stock_warehouse_orderpoint"/>
            <field name="state">code</field>
            <field name="code">model.update_min_max_forecast()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>
            <field name="numbercall">-1</field>
            <field name="active">True</field>
        </record>
    </data>
</odoo>
