from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageEnhance, ImageFilter

IMAGE_PATH = r"D:\kiri-ocr-test\my_id_card.jpg"

OUT_DIR = Path(r"D:\kiri-ocr-test\my_id_fields_enhanced")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_PATH = r"D:\kiri-ocr-test\my_id_enhanced_debug_boxes.jpg"

img = Image.open(IMAGE_PATH).convert("RGB")
print("Image size:", img.size)

# Manual boxes for your current real ID image.
# If a crop is still wrong, we adjust these later.
crops = {
    "khmer_name":        (475, 170, 760, 220),
    "latin_name":        (505, 215, 760, 255),
    "id_number_top":     (800, 120, 1045, 170),

    "birth_gender":      (430, 255, 1120, 305),
    "birth_place":       (430, 300, 1120, 350),

    "address_line_1":    (430, 345, 1120, 395),
    "address_line_2":    (430, 390, 1120, 440),

    "validity_line":     (430, 470, 1120, 520),
    "physical_marks":    (430, 510, 1120, 555),

    "mrz_line_1":        (250, 610, 1130, 665),
    "mrz_line_2":        (250, 655, 1130, 710),
    "mrz_line_3":        (250, 700, 1130, 760),
}

def enhance_crop(crop):
    # Add padding
    crop = ImageOps.expand(crop, border=20, fill=(245, 248, 235))

    # Upscale: OCR works better with bigger text
    crop = crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS)

    # Improve contrast and sharpness
    crop = ImageEnhance.Contrast(crop).enhance(1.8)
    crop = ImageEnhance.Sharpness(crop).enhance(2.0)

    # Light denoise / sharpen
    crop = crop.filter(ImageFilter.UnsharpMask(radius=1.2, percent=160, threshold=3))

    return crop

for name, box in crops.items():
    crop = img.crop(box)
    crop = enhance_crop(crop)

    out_path = OUT_DIR / f"{name}.jpg"
    crop.save(out_path, quality=95)

    print(name, box, "->", out_path)

# Debug image with boxes
debug = img.copy()
draw = ImageDraw.Draw(debug)

for name, box in crops.items():
    draw.rectangle(box, outline="red", width=3)
    draw.text((box[0], max(0, box[1] - 18)), name, fill="red")

debug.save(DEBUG_PATH, quality=95)
print("Debug image saved:", DEBUG_PATH)