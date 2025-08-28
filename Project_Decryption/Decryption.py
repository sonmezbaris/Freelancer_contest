"""
ISBN doğrulama: "059035342X" ISBN-10 geçerli mi diye kontrol ediliyor.

Koordinat dönüşümü: Latitude ve longitude decimal → derece/dakika/saniye (DMS) formatına çevriliyor.

Base64 çözme: Önceden tanımlı Base64 kodları çözülüyor; ASCII karakterleri gösteriliyor, çözülemeyenler binary olarak yazdırılıyor.

Marauder’s Map: 4 karakter ve takma isimleri listeleniyor, ünlü sözler referans olarak ekrana basılıyor.

Final çözüm: Puzzle tipi, yıl, lokasyon, tema ve ISBN referansı yazdırılıyor, çözüm durumu "MISCHIEF MANAGED!" olarak gösteriliyor.

"""
import base64
import math
from typing import Tuple

# Base64 decoding table (not strictly needed, using Python's base64)
BASE64_TABLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def base64_decode(s: str) -> bytes:
    """
    Decode a Base64 string to raw bytes.
    Mirrors the C logic but leverages Python's base64 (ignores whitespace).
    Returns raw bytes; caller can decide how to render them.
    """
    try:
        # validate=False allows non-alphabet chars like newlines/spaces to be ignored
        return base64.b64decode(s, validate=False)
    except Exception:
        # on error, mimic "Decoding failed or binary data" by returning empty bytes
        return b""


def validate_isbn10(isbn: str) -> bool:
    """
    Validate ISBN-10 (checksum mod 11).
    """
    if len(isbn) != 10:
        return False
    total = 0
    for i in range(9):
        if not isbn[i].isdigit():
            return False
        total += int(isbn[i]) * (10 - i)
    last = isbn[9]
    if last in ("X", "x"):
        total += 10
    elif last.isdigit():
        total += int(last)
    else:
        return False
    return total % 11 == 0


def decimal_to_dms(decimal: float) -> Tuple[int, int, float]:
    """
    Convert decimal degrees to degrees/minutes/seconds (DMS).
    """
    degrees = int(decimal)
    temp = (decimal - degrees) * 60.0
    minutes = int(temp)
    seconds = (temp - minutes) * 60.0
    return degrees, minutes, seconds


def print_bytes_human(b: bytes) -> None:
    """
    Print bytes, ASCII if printable (32..126), otherwise as \xHH,
    matching the spirit of the C code.
    """
    out = []
    for ch in b:
        if 32 <= ch <= 126:
            out.append(chr(ch))
        else:
            out.append(f"\\x{ch:02x}")
    print(" └─ Decoded: " + "".join(out))


def main():
    print("=== HARRY POTTER CHALLENGE COIN SOLVER ===\n")

    # Step 1: ISBN Analysis
    print("STEP 1: ISBN VALIDATION")
    print("------------------------")
    isbn = "059035342X"
    print(f"ISBN found on coin: {isbn}")
    if validate_isbn10(isbn):
        print("✓ Valid ISBN-10 format")
        print("✓ This is: Harry Potter and the Sorcerer's Stone")
    else:
        print("✗ Invalid ISBN format")
    print()

    # Step 2: Coordinate Analysis
    print("STEP 2: COORDINATE ANALYSIS")
    print("---------------------------")
    latitude = 59.035342
    longitude = 13.6
    lat_deg, lat_min, lat_sec = decimal_to_dms(latitude)
    lon_deg, lon_min, lon_sec = decimal_to_dms(longitude)
    print(f"Coordinates: {latitude:.6f}, {longitude:.1f}")
    print(
        f'DMS Format: {lat_deg}°{lat_min}\'{lat_sec:.2f}"N, '
        f'{lon_deg}°{lon_min}\'{lon_sec:.2f}"E'
    )
    print("Location: Trollhättan, Sweden (Trollywood film district)")
    print()

    # Step 3: Base64 Decoding
    print("STEP 3: BASE64 DECODING")
    print("-----------------------")
    base64_codes = [
        "VGbzB2i9Wcg",
        "N3IGIu1ScAdk9Xa",
        "vKIvVmc0=0xmTrBONCY",  # Contains "BONCY"
        "vFW Gdutma=",
        "UvB2du9y53eU1w",
        "GdwU3cu",
    ]
    for idx, code in enumerate(base64_codes, start=1):
        print(f"Code {idx}: {code}")
        if idx == 3:
            print(" └─ Contains 'BONCY' - likely event codename")
            print(" └─ Contains '0x' - hexadecimal notation")
            continue

        decoded = base64_decode(code)
        if decoded:
            print_bytes_human(decoded)
        else:
            print(" └─ Decoding failed or binary data")
    print()

    # Step 4: Marauder's Map Analysis
    print("STEP 4: MARAUDER'S MAP FOOTPRINTS")
    print("----------------------------------")
    marauders = [
        "James Potter (Prongs - Stag)",
        "Sirius Black (Padfoot - Dog)",
        "Remus Lupin (Moony - Werewolf)",
        "Peter Pettigrew (Wormtail - Rat)",
    ]
    print("4 stick figures represent the 4 Marauders:")
    for i, m in enumerate(marauders, start=1):
        print(f"{i}. {m}")
    print('\nReference: "I solemnly swear that I am up to no good"')
    print('Complete: "Mischief Managed"\n')

    # Step 5: Final Solution
    print("STEP 5: COMPLETE SOLUTION")
    print("-------------------------")
    print("Puzzle Type: Harry Potter Geocaching Challenge Coin")
    print("Event Year: 2024")
    print("Location: Trollhättan, Sweden")
    print("Theme: Marauder's Map")
    print("ISBN Reference: Harry Potter and the Sorcerer's Stone")
    print("\nMission: Visit coordinates, decode messages, follow Marauders' footsteps")
    print("Status: PUZZLE SOLVED ✓\n")
    print("=== MISCHIEF MANAGED! ===")


if __name__ == "__main__":
    main()
