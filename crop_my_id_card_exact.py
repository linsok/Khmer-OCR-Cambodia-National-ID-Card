from pathlib import Path
from PIL import Image, ImageDraw

IMAGE_PATH = r"D:\kiri-ocr-test\my_id_card.jpg"

OUT_DIR = Path(r"D:\kiri-ocr-test\my_id_fields_exact")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_PATH = r"D:\kiri-ocr-test\my_id_debug_exact.jpg"

# Reference based on the clean card image layout.
# It will scale automatically to your real image size.
REF_W = 649
REF_H = 413

manual_boxes = {
    # Top ID number
    "id_number_top":   (425, 15, 575, 62),

    # Name fields
    "khmer_name":      (145, 38, 415, 78),
    "latin_name":      (250, 68, 405, 100),

    # Main Khmer lines
    "birth_gender":    (145, 88, 630, 125),
    "birth_place":     (145, 118, 630, 155),
    "address_line_1":  (145, 148, 630, 185),
    "address_line_2":  (145, 178, 630, 215),

    # Validity and physical marks
    "validity_line":   (145, 205, 630, 240),
    "physical_marks":  (145, 230, 640, 265),

    # MRZ lines
    "mrz_line_1":      (15, 275, 645, 315),
    "mrz_line_2":      (15, 312, 645, 352),
    "mrz_line_3":      (15, 348, 645, 392),
}

img = Image.open(IMAGE_PATH).convert("RGB")
img_w, img_h = img.size

scale_x = img_w / REF_W
scale_y = img_h / REF_H

print("Image size:", img_w, img_h)
print("scale_x:", scale_x)
print("scale_y:", scale_y)

def scale_box(box):
    x1, y1, x2, y2 = box
    return (
        max(0, int(x1 * scale_x)),
        max(0, int(y1 * scale_y)),
        min(img_w, int(x2 * scale_x)),
        min(img_h, int(y2 * scale_y)),
    )

scaled_boxes = {}

for name, box in manual_boxes.items():
    sbox = scale_box(box)
    scaled_boxes[name] = sbox

    crop = img.crop(sbox)
    out_path = OUT_DIR / f"{name}.jpg"
    crop.save(out_path, quality=95)

    print(f"{name} {sbox} -> {out_path}")

debug = img.copy()
draw = ImageDraw.Draw(debug)

for name, box in scaled_boxes.items():
    draw.rectangle(box, outline="red", width=2)
    draw.text((box[0], max(0, box[1] - 14)), name, fill="red")

debug.save(DEBUG_PATH, quality=95)
print("Debug image saved:", DEBUG_PATH)