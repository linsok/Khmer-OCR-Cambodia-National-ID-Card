from PIL import Image, ImageOps
from pathlib import Path

IMG_PATH = Path("real_tests/my_id_card.jpg")
OUT_DIR = Path("real_tests")
OUT_DIR.mkdir(exist_ok=True)

img = Image.open(IMG_PATH).convert("RGB")

# Boxes from your full-card OCR result:
# format: x, y, width, height
boxes = {
    "name.jpg": (137, 34, 246, 29),
    "id_number.jpg": (418, 10, 145, 31),
    "latin_name.jpg": (263, 64, 106, 24),
    "dob_gender_height.jpg": (148, 81, 478, 29),
    "birth_place.jpg": (146, 110, 375, 29),
    "address_1.jpg": (146, 137, 159, 32),
    "address_2.jpg": (138, 170, 281, 31),
    "validity.jpg": (150, 202, 353, 26),
    "body_mark_left.jpg": (16, 215, 95, 32),
    "body_mark.jpg": (149, 225, 404, 26),
    "mrz_1.jpg": (9, 273, 624, 35),
    "mrz_2.jpg": (9, 309, 623, 34),
    "mrz_3.jpg": (8, 343, 627, 37),
}

def crop_box(img, box, pad_x=8, pad_y=5, scale=2):
    x, y, bw, bh = box

    left = max(0, x - pad_x)
    top = max(0, y - pad_y)
    right = min(img.width, x + bw + pad_x)
    bottom = min(img.height, y + bh + pad_y)

    crop = img.crop((left, top, right, bottom))

    # Add soft padding
    crop = ImageOps.expand(crop, border=8, fill=(245, 248, 238))

    # Upscale moderately
    cw, ch = crop.size
    crop = crop.resize((cw * scale, ch * scale), Image.Resampling.LANCZOS)

    return crop

for name, box in boxes.items():
    crop = crop_box(img, box)
    out_path = OUT_DIR / name
    crop.save(out_path, quality=95)
    print("Saved:", out_path, crop.size)