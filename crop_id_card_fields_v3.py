from pathlib import Path
from PIL import Image, ImageOps

IMAGE_PATH = r"D:\kiri-ocr-test\my_id_card.jpg"

OUT_DIR = Path(r"D:\kiri-ocr-test\my_id_fields")
OUT_DIR.mkdir(parents=True, exist_ok=True)

img = Image.open(IMAGE_PATH).convert("RGB")
print("Image size:", img.size)

# Tighter crop boxes
crops = {
    "khmer_name":        (335, 160, 555, 205),
    "latin_name":        (385, 205, 545, 240),
    "id_number_top":     (685, 130, 920, 185),

    "birth_gender":      (335, 235, 880, 275),
    "birth_place":       (335, 268, 900, 310),

    "address_line_1":    (335, 305, 900, 342),
    "address_line_2":    (335, 338, 900, 376),

    # Tighter validity line only
    "validity_line":     (335, 375, 900, 410),

    # Separate physical marks line
    "physical_marks":    (335, 410, 900, 452),

    "mrz_line_1":        (150, 488, 920, 535),
    "mrz_line_2":        (150, 532, 920, 580),
    "mrz_line_3":        (150, 575, 920, 625),
}

def preprocess_crop(crop):
    return ImageOps.expand(crop, border=12, fill=(245, 248, 235))

for name, box in crops.items():
    crop = img.crop(box)
    crop = preprocess_crop(crop)
    out_path = OUT_DIR / f"{name}.jpg"
    crop.save(out_path, quality=95)
    print(name, box, "->", out_path)