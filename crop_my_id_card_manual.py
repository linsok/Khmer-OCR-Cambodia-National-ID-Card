from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

IMAGE_PATH = r"D:\kiri-ocr-test\my_id_card.jpg"

OUT_DIR = Path(r"D:\kiri-ocr-test\my_id_fields_manual")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_PATH = r"D:\kiri-ocr-test\my_id_manual_debug_boxes.jpg"

img = Image.open(IMAGE_PATH).convert("RGB")
print("Image size:", img.size)

# Manual boxes adjusted for your 1280 x 909 image.
# Format: left, top, right, bottom
crops = {
    # Top information
    "khmer_name":        (475, 170, 760, 220),
    "latin_name":        (505, 215, 760, 255),
    "id_number_top":     (800, 120, 1045, 170),

    # Main Khmer fields
    "birth_gender":      (430, 255, 1120, 305),
    "birth_place":       (430, 300, 1120, 350),
    "address_line_1":    (430, 345, 1120, 395),
    "address_line_2":    (430, 390, 1120, 440),
    "validity_line":     (430, 470, 1120, 520),
    "physical_marks":    (430, 510, 1120, 555),

    # MRZ lines
    "mrz_line_1":        (250, 610, 1130, 665),
    "mrz_line_2":        (250, 655, 1130, 710),
    "mrz_line_3":        (250, 700, 1130, 760),
}

def preprocess_crop(crop):
    return ImageOps.expand(crop, border=12, fill=(245, 248, 235))

# Save crops
for name, box in crops.items():
    crop = img.crop(box)
    crop = preprocess_crop(crop)

    out_path = OUT_DIR / f"{name}.jpg"
    crop.save(out_path, quality=95)

    print(name, box, "->", out_path)

# Save debug image
debug = img.copy()
draw = ImageDraw.Draw(debug)

for name, box in crops.items():
    draw.rectangle(box, outline="red", width=3)
    draw.text((box[0], max(0, box[1] - 18)), name, fill="red")

debug.save(DEBUG_PATH, quality=95)
print("Debug image saved:", DEBUG_PATH)