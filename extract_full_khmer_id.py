from pathlib import Path
import json
import re
from PIL import Image, ImageOps

from kiri_ocr import OCR
from postprocess_id_ocr import postprocess_field


MODEL_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v11_realid_fix\model.safetensors"

# Change this to test another ID card
CARD_IMAGE = Path(r"D:\kiri-ocr-finetune\kiri-ocr\real_tests\my.jpg")
OUT_DIR = Path(r"D:\kiri-ocr-finetune\kiri-ocr\real_tests\auto_crops")
OUT_DIR.mkdir(parents=True, exist_ok=True)


FIELD_BOXES = {
    # Percent coordinates: left, top, right, bottom
    # Tuned from your tested card layout.
    "name": (0.21, 0.08, 0.62, 0.17),
    "id_number": (0.64, 0.02, 0.91, 0.12),
    "latin_name": (0.40, 0.14, 0.59, 0.22),

    "dob_gender_height": (0.22, 0.19, 0.98, 0.29),
    "birth_place": (0.22, 0.28, 0.86, 0.38),
    "address_1": (0.22, 0.36, 0.60, 0.45),
    "address_2": (0.20, 0.43, 0.75, 0.52),

    "validity": (0.22, 0.50, 0.82, 0.58),
    "body_mark_left": (0.02, 0.54, 0.20, 0.64),
    "body_mark": (0.22, 0.56, 0.92, 0.65),

    "mrz_1": (0.00, 0.68, 1.00, 0.78),
    "mrz_2": (0.00, 0.76, 1.00, 0.87),
    "mrz_3": (0.00, 0.84, 1.00, 0.96),
}


POSTPROCESS_FIELD_MAP = {
    "name": "name",
    "id_number": "id_number",
    "latin_name": "latin_name",
    "dob_gender_height": "dob_gender_height",
    "birth_place": "birth_place",
    "address_1": "address",
    "address_2": "address",
    "validity": "validity",
    "body_mark_left": "body_mark",
    "body_mark": "body_mark",
    "mrz_1": "mrz_1",
    "mrz_2": "mrz_2",
    "mrz_3": "mrz_3",
}


def crop_field(img, box, field_name, scale=2, pad=8):
    w, h = img.size
    left = int(box[0] * w)
    top = int(box[1] * h)
    right = int(box[2] * w)
    bottom = int(box[3] * h)

    crop = img.crop((left, top, right, bottom))
    crop = ImageOps.expand(crop, border=pad, fill=(245, 248, 238))

    cw, ch = crop.size
    crop = crop.resize((cw * scale, ch * scale), Image.Resampling.LANCZOS)

    out_path = OUT_DIR / f"{field_name}.jpg"
    crop.save(out_path, quality=95)

    return out_path


def extract_date(text):
    m = re.search(r"[០-៩]{2}\.[០-៩]{2}\.[០-៩]{4}", text)
    return m.group(0) if m else ""


def extract_all_dates(text):
    return re.findall(r"[០-៩]{2}\.[០-۹]{2}\.[۰-۹]{4}", text)


def extract_all_dates_safe(text):
    return re.findall(r"[០-៩]{2}\.[۰-۹]{2}\.[۰-۹]{4}|[۰-۹]{2}\.[۰-۹]{2}\.[۰-۹]{4}", text)


def extract_height(text):
    m = re.search(r"[۰-۹០-៩]{3}\s*ស\.ម", text)
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
    if not CARD_IMAGE.exists():
        raise FileNotFoundError(f"Card image not found: {CARD_IMAGE}")

    img = Image.open(CARD_IMAGE).convert("RGB")
    print("Card image:", CARD_IMAGE)
    print("Image size:", img.size)

    ocr = OCR(
        model_path=MODEL_PATH,
        device="cpu",
        decode_method="beam",
    )

    raw = {}
    clean = {}
    crop_paths = {}

    for field_name, box in FIELD_BOXES.items():
        crop_path = crop_field(img, box, field_name)
        crop_paths[field_name] = str(crop_path)

        text, results = ocr.extract_text(str(crop_path))
        raw_text = text.strip().replace("\n", " ")

        post_field = POSTPROCESS_FIELD_MAP.get(field_name, field_name)
        clean_text = postprocess_field(post_field, raw_text)

        raw[field_name] = raw_text
        clean[field_name] = clean_text

    dob_line = clean.get("dob_gender_height", "")
    validity_line = clean.get("validity", "")
    validity_dates = extract_all_dates_safe(validity_line)

    result = {
        "name_kh": remove_label(clean.get("name", ""), ["គោត្តនាមនិងនាម"]),
        "id_number": clean.get("id_number", ""),
        "latin_name": clean.get("latin_name", ""),
        "dob": extract_date(dob_line),
        "gender": extract_gender(dob_line),
        "height": extract_height(dob_line),
        "birth_place": remove_label(clean.get("birth_place", ""), ["ទីកន្លែងកំណើត"]),
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
        "debug_crop_paths": crop_paths,
        "debug_raw_ocr": raw,
        "debug_clean_ocr": clean,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    out_json = CARD_IMAGE.with_name(CARD_IMAGE.stem + "_extracted.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\nSaved:", out_json)
    print("Crops saved in:", OUT_DIR)


if __name__ == "__main__":
    main()