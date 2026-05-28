from pathlib import Path
from PIL import Image, ImageDraw

IMAGE_PATH = r"D:\kiri-ocr-test\my_id_card.jpg"

OUT_DIR = Path(r"D:\kiri-ocr-test\my_id_fields_manual_v9")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_PATH = r"D:\kiri-ocr-test\my_id_debug_manual_v9.jpg"

REF_W = 1280
REF_H = 909

manual_boxes = {
    "id_number_top":   (720, 28, 1200, 112),

    "khmer_name":      (300, 82, 840, 148),
    "latin_name":      (410, 138, 890, 198),

    "birth_gender":    (300, 188, 1278, 248),
    "birth_place":     (300, 248, 1278, 308),

    "address_line_1":  (300, 308, 1278, 368),
    "address_line_2":  (300, 386, 1278, 446),

    # moved downward
    "validity_line":   (300, 458, 1278, 518),

    # moved downward
    "physical_marks":  (300, 518, 1278, 586),

    "mrz_line_1":      (20, 628, 1278, 688),
    "mrz_line_2":      (20, 690, 1278, 750),
    "mrz_line_3":      (20, 752, 1278, 815),
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
    draw.rectangle(box, outline="red", width=3)
    label_y = max(0, box[1] - 22)
    draw.text((box[0], label_y), name, fill="red")

debug.save(DEBUG_PATH, quality=95)
print("Debug image saved:", DEBUG_PATH)