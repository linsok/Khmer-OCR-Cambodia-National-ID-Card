from pathlib import Path
from PIL import Image, ImageDraw

# ==============================
# INPUT / OUTPUT
# ==============================
IMAGE_PATH = r"D:\kiri-ocr-test\my_id_card.jpg"
OUT_DIR = Path(r"D:\kiri-ocr-test\my_id_fields_manual_v2")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_PATH = r"D:\kiri-ocr-test\my_id_debug_manual_v2.jpg"

# ==============================
# REFERENCE IMAGE SIZE
# These boxes are estimated for your card layout
# based on the screenshot you showed.
# If the real image size differs, boxes will scale.
# ==============================
REF_W = 1280
REF_H = 909

# ==============================
# MANUALLY TUNED BOXES
# Format: (x1, y1, x2, y2)
# These are spaced apart more cleanly.
# ==============================
manual_boxes = {
    "id_number_top":   (760, 120, 1110, 185),

    "khmer_name":      (350, 155, 735, 205),
    "latin_name":      (440, 205, 760, 245),

    "birth_gender":    (350, 248, 1120, 292),
    "birth_place":     (350, 292, 1120, 336),

    "address_line_1":  (350, 336, 1120, 380),
    "address_line_2":  (350, 380, 1120, 424),

    "validity_line":   (350, 458, 1120, 502),
    "physical_marks":  (350, 502, 1120, 548),

    "mrz_line_1":      (150, 610, 1140, 665),
    "mrz_line_2":      (150, 665, 1140, 720),
    "mrz_line_3":      (150, 720, 1140, 775),
}

# ==============================
# LOAD IMAGE
# ==============================
img = Image.open(IMAGE_PATH).convert("RGB")
img_w, img_h = img.size

scale_x = img_w / REF_W
scale_y = img_h / REF_H

print("Image size:", img_w, img_h)
print("scale_x:", scale_x)
print("scale_y:", scale_y)

def scale_box(box):
    x1, y1, x2, y2 = box
    sx1 = int(x1 * scale_x)
    sy1 = int(y1 * scale_y)
    sx2 = int(x2 * scale_x)
    sy2 = int(y2 * scale_y)

    sx1 = max(0, sx1)
    sy1 = max(0, sy1)
    sx2 = min(img_w, sx2)
    sy2 = min(img_h, sy2)

    return (sx1, sy1, sx2, sy2)

# ==============================
# CROP AND SAVE
# ==============================
scaled_boxes = {}

for name, box in manual_boxes.items():
    sbox = scale_box(box)
    scaled_boxes[name] = sbox

    crop = img.crop(sbox)
    out_path = OUT_DIR / f"{name}.jpg"
    crop.save(out_path, quality=95)

    print(f"{name} {sbox} -> {out_path}")

# ==============================
# SAVE DEBUG IMAGE
# ==============================
debug = img.copy()
draw = ImageDraw.Draw(debug)

for name, box in scaled_boxes.items():
    draw.rectangle(box, outline="red", width=3)

    tx = box[0]
    ty = max(0, box[1] - 18)
    draw.text((tx, ty), name, fill="red")

debug.save(DEBUG_PATH, quality=95)
print("Debug image saved:", DEBUG_PATH)