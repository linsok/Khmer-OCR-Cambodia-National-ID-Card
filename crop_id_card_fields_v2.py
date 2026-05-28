from pathlib import Path
from PIL import Image, ImageOps

IMAGE_PATH = r"D:\kiri-ocr-test\id_card.jpg"

OUT_DIR = Path(r"D:\kiri-ocr-test\id_fields_v2")
OUT_DIR.mkdir(parents=True, exist_ok=True)

img = Image.open(IMAGE_PATH).convert("RGB")
print("Image size:", img.size)

# Better crop boxes for the uploaded image size around 1114 x 768
# Format: left, top, right, bottom
crops = {
    # Top fields
    "khmer_name":        (335, 160, 555, 205),
    "latin_name":        (385, 205, 545, 240),
    "id_number_top":     (685, 130, 920, 185),

    # Main Khmer fields
    "birth_gender":      (335, 235, 880, 275),
    "birth_place":       (335, 268, 900, 310),

    # Address field seems to start below birth place
    "address_line_1":    (335, 305, 900, 345),
    "address_line_2":    (335, 335, 900, 375),

    # Issue and expiry line
    "issue_expiry":      (335, 375, 900, 420),

    # Physical marks line
    "physical_marks":    (335, 415, 900, 455),

    # MRZ lines
    "mrz_line_1":        (150, 488, 920, 535),
    "mrz_line_2":        (150, 532, 920, 580),
    "mrz_line_3":        (150, 575, 920, 625),
}

def preprocess_crop(crop):
    # Add white padding so detector sees full line
    crop = ImageOps.expand(crop, border=12, fill=(245, 248, 235))
    return crop

for name, box in crops.items():
    crop = img.crop(box)
    crop = preprocess_crop(crop)
    out_path = OUT_DIR / f"{name}.jpg"
    crop.save(out_path, quality=95)
    print(name, box, "->", out_path)