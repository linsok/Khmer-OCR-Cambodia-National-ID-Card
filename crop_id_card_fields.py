from pathlib import Path
from PIL import Image

# Change this to your image location on your computer
IMAGE_PATH = r"D:\kiri-ocr-test\id_card.jpg"

OUT_DIR = Path(r"D:\kiri-ocr-test\id_fields")
OUT_DIR.mkdir(parents=True, exist_ok=True)

img = Image.open(IMAGE_PATH)
w, h = img.size

print("Image size:", w, h)

# These crop boxes are estimated for your uploaded ID-card-style image.
# Format: (left, top, right, bottom)
crops = {
    "khmer_name":      (330, 165, 560, 215),
    "latin_name":      (390, 205, 540, 245),
    "birth_gender":    (330, 235, 870, 275),
    "birth_place":     (330, 270, 870, 315),
    "address_1":       (330, 310, 870, 355),
    "address_2":       (330, 350, 870, 395),
    "issue_expiry":    (330, 390, 870, 430),
    "id_number_top":   (680, 135, 920, 185),
    "mrz_line_1":      (150, 490, 910, 535),
    "mrz_line_2":      (150, 535, 910, 580),
    "mrz_line_3":      (150, 575, 910, 625),
}

for name, box in crops.items():
    crop = img.crop(box)
    out_path = OUT_DIR / f"{name}.jpg"
    crop.save(out_path, quality=95)
    print("Saved:", out_path)