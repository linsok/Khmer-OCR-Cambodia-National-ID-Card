from pathlib import Path
from PIL import Image, ImageOps
from kiri_ocr import OCR

MODEL_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v11_realid_fix\model.safetensors"
CARD_IMAGE = Path(r"D:\kiri-ocr-finetune\kiri-ocr\real_tests\test_card_2.jpg")

OUT_DIR = Path(r"D:\kiri-ocr-finetune\kiri-ocr\real_tests\debug_lines_card2")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ocr = OCR(
    model_path=MODEL_PATH,
    device="cpu",
    decode_method="beam",
)

text, results = ocr.extract_text(str(CARD_IMAGE))

print("\nFULL OCR TEXT:")
print(text)

print("\nDETECTED LINES:")
img = Image.open(CARD_IMAGE).convert("RGB")

for i, r in enumerate(results, start=1):
    box = r.get("box")
    line_text = r.get("text", "")
    conf = r.get("confidence")
    det_conf = r.get("det_confidence")

    print(f"\nLine {i}")
    print("Box:", box)
    print("Text:", line_text)
    print("OCR confidence:", conf)
    print("Detection confidence:", det_conf)

    if not box:
        continue

    x, y, w, h = box

    pad_x = 10
    pad_y = 6

    left = max(0, x - pad_x)
    top = max(0, y - pad_y)
    right = min(img.width, x + w + pad_x)
    bottom = min(img.height, y + h + pad_y)

    crop = img.crop((left, top, right, bottom))
    crop = ImageOps.expand(crop, border=8, fill=(245, 248, 238))

    out_path = OUT_DIR / f"line_{i:02d}.jpg"
    crop.save(out_path, quality=95)

print("\nSaved detected line crops to:", OUT_DIR)