from pathlib import Path
from PIL import Image, ImageOps
from kiri_ocr import OCR

MODEL_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v11_realid_fix\model.safetensors"

CARD_DIR = Path("real_tests/real_cards")
OUT_DIR = Path("data/khmer_real_card_lines_v1")
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

ocr = OCR(
    model_path=MODEL_PATH,
    device="cpu",
    decode_method="beam",
)

label_suggestion_path = OUT_DIR / "label_suggestions.txt"

all_rows = []
counter = 0

for card_path in sorted(CARD_DIR.glob("*")):
    if card_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
        continue

    print("\nProcessing:", card_path)

    img = Image.open(card_path).convert("RGB")
    text, results = ocr.extract_text(str(card_path))

    # Sort lines top-to-bottom, left-to-right
    results = sorted(
        results,
        key=lambda r: (
            r.get("box", [0, 0, 0, 0])[1],
            r.get("box", [0, 0, 0, 0])[0],
        ),
    )

    for i, r in enumerate(results, start=1):
        box = r.get("box")
        pred_text = r.get("text", "").strip()

        if not box:
            continue

        x, y, w, h = box

        pad_x = 12
        pad_y = 8

        left = max(0, x - pad_x)
        top = max(0, y - pad_y)
        right = min(img.width, x + w + pad_x)
        bottom = min(img.height, y + h + pad_y)

        crop = img.crop((left, top, right, bottom))
        crop = ImageOps.expand(crop, border=8, fill=(245, 248, 238))

        counter += 1
        filename = f"realcard_{card_path.stem}_line_{i:02d}_{counter:04d}.jpg"
        crop_path = IMG_DIR / filename
        crop.save(crop_path, quality=95)

        rel_path = f"images/{filename}"
        all_rows.append(f"{rel_path}\t{pred_text}")

        print(f"  saved {filename}: {pred_text}")

with open(label_suggestion_path, "w", encoding="utf-8") as f:
    for row in all_rows:
        f.write(row + "\n")

print("\nDone.")
print("Total line crops:", len(all_rows))
print("Suggestions saved to:", label_suggestion_path)
print("Images saved to:", IMG_DIR)