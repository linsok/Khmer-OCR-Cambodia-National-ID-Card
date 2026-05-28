from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

IMAGE_PATH = r"D:\kiri-ocr-test\my_id_card.jpg"

OUT_DIR = Path(r"D:\kiri-ocr-test\my_id_fields_scaled")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_PATH = r"D:\kiri-ocr-test\my_id_debug_boxes.jpg"

img = Image.open(IMAGE_PATH).convert("RGB")
w, h = img.size

print("Image size:", w, h)

# Original boxes were made for this sample size
BASE_W = 1114
BASE_H = 800

scale_x = w / BASE_W
scale_y = h / BASE_H

print("scale_x:", scale_x)
print("scale_y:", scale_y)

# Base crop boxes from the good sample image
base_crops = {
    "khmer_name":        (335, 160, 555, 205),
    "latin_name":        (385, 205, 545, 240),
    "id_number_top":     (685, 130, 920, 185),

    "birth_gender":      (335, 235, 880, 275),
    "birth_place":       (335, 268, 900, 310),

    "address_line_1":    (335, 305, 900, 342),
    "address_line_2":    (335, 338, 900, 376),

    "validity_line":     (335, 375, 900, 410),
    "physical_marks":    (335, 410, 900, 452),

    "mrz_line_1":        (150, 488, 920, 535),
    "mrz_line_2":        (150, 532, 920, 580),
    "mrz_line_3":        (150, 575, 920, 625),
}

def scale_box(box):
    left, top, right, bottom = box
    return (
        int(left * scale_x),
        int(top * scale_y),
        int(right * scale_x),
        int(bottom * scale_y),
    )

def preprocess_crop(crop):
    return ImageOps.expand(crop, border=12, fill=(245, 248, 235))

# Save crops
for name, base_box in base_crops.items():
    box = scale_box(base_box)
    crop = img.crop(box)
    crop = preprocess_crop(crop)

    out_path = OUT_DIR / f"{name}.jpg"
    crop.save(out_path, quality=95)

    print(name, box, "->", out_path)

# Save debug image with boxes drawn
debug = img.copy()
draw = ImageDraw.Draw(debug)

for name, base_box in base_crops.items():
    box = scale_box(base_box)
    draw.rectangle(box, outline="red", width=3)
    draw.text((box[0], max(0, box[1] - 18)), name, fill="red")

debug.save(DEBUG_PATH, quality=95)
print("Debug image saved:", DEBUG_PATH)