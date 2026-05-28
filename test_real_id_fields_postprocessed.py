from pathlib import Path
from kiri_ocr import OCR
from postprocess_id_ocr import postprocess_field

MODEL_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v11_realid_fix\model.safetensors"
IMAGE_DIR = Path(r"D:\kiri-ocr-finetune\kiri-ocr\real_tests")

FIELD_MAP = {
    "name.jpg": "name",
    "id_number.jpg": "id_number",
    "latin_name.jpg": "latin_name",
    "dob_gender_height.jpg": "dob_gender_height",
    "birth_place.jpg": "birth_place",
    "address_1.jpg": "address",
    "address_2.jpg": "address",
    "validity.jpg": "validity",
    "body_mark_left.jpg": "body_mark",
    "body_mark.jpg": "body_mark",
    "mrz_1.jpg": "mrz_1",
    "mrz_2.jpg": "mrz_2",
    "mrz_3.jpg": "mrz_3",
}

ocr = OCR(
    model_path=MODEL_PATH,
    device="cpu",
    decode_method="beam",
)

for img_name, field_name in FIELD_MAP.items():
    img_path = IMAGE_DIR / img_name

    if not img_path.exists():
        print(f"\nMissing: {img_path}")
        continue

    text, results = ocr.extract_text(str(img_path))
    raw_text = text.strip().replace("\n", " ")

    clean_text = postprocess_field(field_name, raw_text)

    print("\n" + "=" * 70)
    print("IMAGE:", img_name)
    print("FIELD:", field_name)
    print("RAW:")
    print(raw_text)
    print("CLEAN:")
    print(clean_text)