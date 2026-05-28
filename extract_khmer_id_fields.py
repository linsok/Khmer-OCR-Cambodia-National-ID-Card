from pathlib import Path
import json
import re

from kiri_ocr import OCR
from postprocess_id_ocr import postprocess_field


MODEL_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v11_realid_fix\model.safetensors"
IMAGE_DIR = Path(r"D:\kiri-ocr-finetune\kiri-ocr\real_tests")


FIELD_FILES = {
    "name": "name.jpg",
    "id_number": "id_number.jpg",
    "latin_name": "latin_name.jpg",
    "dob_gender_height": "dob_gender_height.jpg",
    "birth_place": "birth_place.jpg",
    "address_1": "address_1.jpg",
    "address_2": "address_2.jpg",
    "validity": "validity.jpg",
    "body_mark_left": "body_mark_left.jpg",
    "body_mark": "body_mark.jpg",
    "mrz_1": "mrz_1.jpg",
    "mrz_2": "mrz_2.jpg",
    "mrz_3": "mrz_3.jpg",
}


def extract_date(text):
    # Khmer date format: ១២.០៩.១៩៨៤
    m = re.search(r"[០-៩]{2}\.[០-៩]{2}\.[០-៩]{4}", text)
    return m.group(0) if m else ""


def extract_all_dates(text):
    return re.findall(r"[០-៩]{2}\.[០-៩]{2}\.[០-៩]{4}", text)


def extract_height(text):
    m = re.search(r"[០-៩]{3}\s*ស\.ម", text)
    return m.group(0).replace(" ", "") if m else ""


def extract_gender(text):
    if "ប្រុស" in text:
        return "ប្រុស"
    if "ស្រី" in text:
        return "ស្រី"
    return ""


def remove_label(text, labels):
    cleaned = text
    for label in labels:
        cleaned = cleaned.replace(label, "")
    cleaned = cleaned.replace(":", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def main():
    ocr = OCR(
        model_path=MODEL_PATH,
        device="cpu",
        decode_method="beam",
    )

    raw = {}
    clean = {}

    for field_name, filename in FIELD_FILES.items():
        img_path = IMAGE_DIR / filename

        if not img_path.exists():
            raw[field_name] = ""
            clean[field_name] = ""
            continue

        text, results = ocr.extract_text(str(img_path))
        raw_text = text.strip().replace("\n", " ")

        # Map related field types to postprocessor names
        post_field = field_name
        if field_name.startswith("address"):
            post_field = "address"
        if field_name.startswith("mrz"):
            post_field = field_name
        if field_name.startswith("body_mark"):
            post_field = "body_mark"

        clean_text = postprocess_field(post_field, raw_text)

        raw[field_name] = raw_text
        clean[field_name] = clean_text

    dob_line = clean.get("dob_gender_height", "")
    validity_line = clean.get("validity", "")

    validity_dates = extract_all_dates(validity_line)

    result = {
        "name_kh": remove_label(
            clean.get("name", ""),
            ["គោត្តនាមនិងនាម"]
        ),
        "id_number": clean.get("id_number", ""),
        "latin_name": clean.get("latin_name", ""),
        "dob": extract_date(dob_line),
        "gender": extract_gender(dob_line),
        "height": extract_height(dob_line),
        "birth_place": remove_label(
            clean.get("birth_place", ""),
            ["ទីកន្លែងកំណើត"]
        ),
        "address": " ".join(
            part for part in [
                remove_label(clean.get("address_1", ""), ["អាសយដ្ឋាន"]),
                clean.get("address_2", ""),
            ]
            if part
        ),
        "valid_from": validity_dates[0] if len(validity_dates) >= 1 else "",
        "valid_to": validity_dates[1] if len(validity_dates) >= 2 else "",
        "body_mark": clean.get("body_mark", ""),
        "mrz": [
            clean.get("mrz_1", ""),
            clean.get("mrz_2", ""),
            clean.get("mrz_3", ""),
        ],
        "debug_raw_ocr": raw,
        "debug_clean_ocr": clean,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    out_path = IMAGE_DIR / "extracted_id_result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\nSaved:", out_path)


if __name__ == "__main__":
    main()