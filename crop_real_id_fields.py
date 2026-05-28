from PIL import Image, ImageOps
from pathlib import Path

IMG_PATH = Path("real_tests/my_id_card.jpg")
OUT_DIR = Path("real_tests")
OUT_DIR.mkdir(exist_ok=True)

img = Image.open(IMG_PATH).convert("RGB")
w, h = img.size

print("Image size:", w, h)

# Adjusted for the sample ID card layout.
# Percent coordinates: left, top, right, bottom
crops = {
    # top text fields
    "name.jpg":              (0.20, 0.07, 0.75, 0.17),
    "id_number.jpg":         (0.64, 0.02, 0.98, 0.12),
    "latin_name.jpg":        (0.38, 0.14, 0.62, 0.23),

    # main Khmer lines
    "dob_gender_height.jpg": (0.20, 0.18, 0.99, 0.29),
    "birth_place.jpg":       (0.20, 0.28, 0.95, 0.38),
    "address_1.jpg":         (0.20, 0.36, 0.95, 0.45),
    "address_2.jpg":         (0.20, 0.43, 0.95, 0.52),

    # separate validity and body mark
    "validity.jpg":          (0.20, 0.50, 0.95, 0.58),
    "body_mark.jpg":         (0.20, 0.56, 0.95, 0.65),

    # MRZ lines: make them full width and taller
    "mrz_1.jpg":             (0.00, 0.68, 1.00, 0.78),
    "mrz_2.jpg":             (0.00, 0.76, 1.00, 0.87),
    "mrz_3.jpg":             (0.00, 0.84, 1.00, 0.96),
}

def crop_pad_upscale(img, box, scale=2, pad=10):
    left = int(box[0] * w)
    top = int(box[1] * h)
    right = int(box[2] * w)
    bottom = int(box[3] * h)

    crop = img.crop((left, top, right, bottom))

    # add white/greenish padding around text
    crop = ImageOps.expand(crop, border=pad, fill=(245, 248, 238))

    # upscale for OCR
    cw, ch = crop.size
    crop = crop.resize((cw * scale, ch * scale), Image.Resampling.LANCZOS)

    return crop

for name, box in crops.items():
    crop = crop_pad_upscale(img, box, scale=2, pad=12)
    out_path = OUT_DIR / name
    crop.save(out_path, quality=95)
    print("Saved:", out_path, crop.size)