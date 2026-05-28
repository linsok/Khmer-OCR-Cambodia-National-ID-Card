from pathlib import Path
from PIL import Image, ImageDraw

IMAGE_PATH = r"D:\kiri-ocr-test\my_id_card.jpg"
OUT_DIR = Path(r"D:\kiri-ocr-test\my_id_fields_scaled_big")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_PATH = r"D:\kiri-ocr-test\my_id_debug_boxes_big.jpg"

# Template size used for original reference card
TEMPLATE_W = 1114
TEMPLATE_H = 800

# Base template boxes from your v3 script
base_boxes = {
    "khmer_name":    (335, 160, 555, 205),
    "latin_name":    (385, 205, 545, 240),
    "id_number_top": (685, 130, 920, 185),

    "birth_gender":  (335, 235, 880, 275),
    "birth_place":   (335, 268, 900, 310),

    "address_line_1": (335, 305, 900, 342),
    "address_line_2": (335, 338, 900, 376),

    "validity_line":  (335, 375, 900, 410),
    "physical_marks": (335, 410, 900, 452),

    "mrz_line_1": (150, 488, 920, 535),
    "mrz_line_2": (150, 532, 920, 580),
    "mrz_line_3": (150, 575, 920, 625),
}

img = Image.open(IMAGE_PATH).convert("RGB")
img_w, img_h = img.size

scale_x = img_w / TEMPLATE_W
scale_y = img_h / TEMPLATE_H

print("Image size:", img_w, img_h)
print("scale_x:", scale_x)
print("scale_y:", scale_y)

def scale_box(box):
    x1, y1, x2, y2 = box
    return (
        int(x1 * scale_x),
        int(y1 * scale_y),
        int(x2 * scale_x),
        int(y2 * scale_y),
    )

def expand_box(box, pad_left=20, pad_top=10, pad_right=20, pad_bottom=10):
    x1, y1, x2, y2 = box
    x1 = max(0, x1 - pad_left)
    y1 = max(0, y1 - pad_top)
    x2 = min(img_w, x2 + pad_right)
    y2 = min(img_h, y2 + pad_bottom)
    return (x1, y1, x2, y2)

# Bigger padding per field
def make_big_box(name, scaled_box):
    if name == "khmer_name":
        return expand_box(scaled_box, 35, 12, 45, 14)

    if name == "latin_name":
        return expand_box(scaled_box, 35, 10, 45, 12)

    if name == "id_number_top":
        return expand_box(scaled_box, 30, 10, 35, 14)

    if name in ["birth_gender", "birth_place", "address_line_1", "address_line_2", "validity_line", "physical_marks"]:
        return expand_box(scaled_box, 35, 12, 55, 14)

    if name in ["mrz_line_1", "mrz_line_2", "mrz_line_3"]:
        return expand_box(scaled_box, 25, 10, 25, 12)

    return expand_box(scaled_box, 20, 10, 20, 10)

final_boxes = {}
for name, box in base_boxes.items():
    scaled = scale_box(box)
    bigger = make_big_box(name, scaled)
    final_boxes[name] = bigger

# Save crops
for name, box in final_boxes.items():
    crop = img.crop(box)
    out_path = OUT_DIR / f"{name}.jpg"
    crop.save(out_path, quality=95)
    print(f"{name} {box} -> {out_path}")

# Save debug image
debug = img.copy()
draw = ImageDraw.Draw(debug)

for name, box in final_boxes.items():
    draw.rectangle(box, outline="red", width=3)
    label_y = max(0, box[1] - 18)
    draw.text((box[0], label_y), name, fill="red")

debug.save(DEBUG_PATH, quality=95)
print("Debug image saved:", DEBUG_PATH)