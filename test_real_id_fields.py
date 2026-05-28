from pathlib import Path
from kiri_ocr import OCR

MODEL_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v11_realid_fix\model.safetensors"
IMAGE_DIR = Path(r"D:\kiri-ocr-finetune\kiri-ocr\real_tests")
IMAGES = [
    "name.jpg",
    "id_number.jpg",
    "latin_name.jpg",
    "dob_gender_height.jpg",
    "birth_place.jpg",
    "address_1.jpg",
    "address_2.jpg",
    "validity.jpg",
    "body_mark_left.jpg",
    "body_mark.jpg",
    "mrz_1.jpg",
    "mrz_2.jpg",
    "mrz_3.jpg",
]

ocr = OCR(
    model_path=MODEL_PATH,
    device="cpu",
    decode_method="beam",
)

for img_name in IMAGES:
    img_path = IMAGE_DIR / img_name

    if not img_path.exists():
        print(f"\nMissing: {img_path}")
        continue

    text, results = ocr.extract_text(str(img_path))

    print("\n" + "=" * 70)
    print("IMAGE:", img_name)
    print("OCR TEXT:")
    print(text)

    print("\nDETAILS:")
    for r in results:
        print(r)