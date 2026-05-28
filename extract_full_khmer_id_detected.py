from pathlib import Path
import json
import re

from kiri_ocr import OCR
from postprocess_id_ocr import postprocess_field


MODEL_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v11_realid_fix\model.safetensors"

# Change this path for each card
CARD_IMAGE = Path(r"D:\kiri-ocr-finetune\kiri-ocr\real_tests\photo_2026-05-28_16-13-20.jpg")


KHMER_DIGITS = "០១២៣៤៥៦៧៨៩"
LATIN_DIGITS = "0123456789"

KHMER_DATE_RE = "[" + KHMER_DIGITS + r"]{2}\.[" + KHMER_DIGITS + r"]{2}\.[" + KHMER_DIGITS + r"]{4}"
KHMER_HEIGHT_WITH_UNIT_RE = "[" + KHMER_DIGITS + r"]{3}\s*ស\.ម"
KHMER_HEIGHT_NUM_RE = "[" + KHMER_DIGITS + r"]{3}"


def khmer_digit_to_latin(text):
    return text.translate(str.maketrans(KHMER_DIGITS, LATIN_DIGITS))


def latin_to_khmer_digits(text):
    return text.translate(str.maketrans(LATIN_DIGITS, KHMER_DIGITS))


def clean_id_number(text):
    text = khmer_digit_to_latin(text)
    text = text.replace("O", "0").replace("o", "0")
    return "".join(ch for ch in text if ch.isdigit())


def clean_latin_name(text):
    text = text.strip().upper()

    # In normal names, 0 is usually OCR confusion for O.
    text = text.replace("0", "O")

    text = re.sub(r"[^A-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_mrz_extra(text, field_name="mrz"):
    # Fix OCR mistakes before MRZ filtering.
    text = text.replace("ឫ", "<")

    if field_name == "mrz_1":
        text = text.replace("O", "0").replace("o", "0")
        text = text.replace("I D", "ID")
        text = text.replace("IDKHMO", "IDKHM0")

    if field_name == "mrz_2":
        # Khmer-looking OCR mistakes inside MRZ2
        text = text.replace("ក", "1")
        text = text.replace("ខ", "1")

    # Do NOT convert O -> 0 in MRZ3 because names like THORN / SOK need O.
    text = postprocess_field(field_name, text)

    if field_name == "mrz_1":
        text = text.replace("IDKHMO", "IDKHM0")

    return text


def extract_date(text):
    m = re.search(KHMER_DATE_RE, text)
    return m.group(0) if m else ""


def extract_all_dates(text):
    return re.findall(KHMER_DATE_RE, text)


def extract_height(text):
    # Prefer number after កម្ពស់ / កំពស់.
    m = re.search(r"(?:កម្ពស់|កំពស់)\s*[:ៈ.]?\s*([" + KHMER_DIGITS + r"]{3})", text)
    if m:
        return m.group(1) + "ស.ម"

    # Fallback: explicit unit.
    m = re.search("[" + KHMER_DIGITS + r"]{3}\s*ស\.ម", text)
    if m:
        return m.group(0).replace(" ", "")

    return ""


def extract_gender(text):
    if "ប្រុស" in text:
        return "ប្រុស"
    if "ស្រី" in text:
        return "ស្រី"
    return ""


def dob_from_mrz2(mrz2):
    """
    MRZ line 2 often starts with DOB in YYMMDD.
    Example: 900803 -> 03.08.1990
    """
    digits = "".join(ch for ch in mrz2 if ch.isdigit())

    if len(digits) < 6:
        return ""

    candidates = [digits[0:6]]

    # If OCR inserted/dropped one digit, try first 7 digits with one skipped.
    if len(digits) >= 7:
        first7 = digits[0:7]
        for skip in range(len(first7)):
            candidates.append(first7[:skip] + first7[skip + 1:])

    for c in candidates:
        if len(c) != 6:
            continue

        yy = int(c[0:2])
        mm = int(c[2:4])
        dd = int(c[4:6])

        if 1 <= mm <= 12 and 1 <= dd <= 31:
            year = 1900 + yy if yy > 25 else 2000 + yy
            return latin_to_khmer_digits(f"{dd:02d}.{mm:02d}.{year}")

    return ""


def expiry_from_mrz2(mrz2):
    """
    Recover expiry date from MRZ line 2.
    Looks for likely YYMMDD from 2025-2035.
    Example: 260125 -> 25.01.2026
    """
    digits = "".join(ch for ch in mrz2 if ch.isdigit())

    if len(digits) < 12:
        return ""

    for i in range(6, len(digits) - 5):
        chunk = digits[i:i + 6]

        yy = int(chunk[0:2])
        mm = int(chunk[2:4])
        dd = int(chunk[4:6])

        if 25 <= yy <= 35 and 1 <= mm <= 12 and 1 <= dd <= 31:
            year = 2000 + yy
            return latin_to_khmer_digits(f"{dd:02d}.{mm:02d}.{year}")

    return ""


def remove_label(text, labels):
    cleaned = text

    for label in labels:
        cleaned = cleaned.replace(label, "")

    cleaned = cleaned.replace(":", " ")
    cleaned = cleaned.replace("ៈ", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def sorted_results(results):
    return sorted(
        results,
        key=lambda r: (
            r.get("box", [0, 0, 0, 0])[1],
            r.get("box", [0, 0, 0, 0])[0],
        ),
    )


def get_text(line):
    return line.get("text", "").strip()


def looks_like_mrz(text):
    t = text.upper().replace(" ", "")

    return (
        "IDKHM" in t
        or "<<" in t
        or ("<" in t and any(ch.isdigit() for ch in t))
        or re.search(r"[A-Z]{2,}<<[A-Z]{2,}", t) is not None
    )


def split_mrz_and_top_lines(lines):
    """
    Dynamic split:
    - MRZ lines are usually bottom lines and contain < or IDKHM.
    - Everything else is normal field text.
    """
    mrz_lines = []
    normal_lines = []

    for line in lines:
        text = get_text(line)

        if looks_like_mrz(text):
            mrz_lines.append(line)
        else:
            normal_lines.append(line)

    mrz_lines = sorted_results(mrz_lines)
    normal_lines = sorted_results(normal_lines)

    return normal_lines, mrz_lines


def get_line_text(lines, idx):
    if idx < len(lines):
        return get_text(lines[idx])
    return ""


def find_first_text(texts, keywords):
    for text in texts:
        for kw in keywords:
            if kw in text:
                return text
    return ""


def find_index(texts, keywords):
    for i, text in enumerate(texts):
        for kw in keywords:
            if kw in text:
                return i
    return -1


def is_latin_name_line(text):
    t = text.strip()

    if not t:
        return False

    if "<<" in t or "<" in t:
        return False

    # Avoid MRZ-like / numeric-heavy lines.
    if any(ch.isdigit() for ch in t) and sum(ch.isalpha() and ch.isascii() for ch in t) < 3:
        return False

    letters = sum(ch.isalpha() and ch.isascii() for ch in t)
    return letters >= 3


def map_normal_lines(normal_lines, mrz_lines):
    """
    Keyword-based field mapping.

    This handles:
    - normal card: DOB/gender/height in one line
    - generated card: DOB, gender, height split into separate lines
    - 12-line / 13-line / 15-line cards
    """
    texts = [get_text(x) for x in normal_lines if get_text(x).strip()]

    id_number = texts[0] if texts else ""

    name = find_first_text(texts, ["គោត្តនាម", "នោត្តនាម", "នាម"])

    latin_name = ""
    for text in texts:
        if is_latin_name_line(text):
            latin_name = text
            break

    dob_idx = find_index(
        texts,
        [
            "ថ្ងៃខែឆ្នាំកំណើត",
            "ថ្ងៃខាំកំណើត",
            "ថ្ងៃខ្នាំកំណើត",
            "ថ្លៃវខ្នាក់ណើត",
            "កំណើត",
        ],
    )

    gender_idx = find_index(texts, ["ភេទ", "គេទ", "កេទ"])
    height_idx = find_index(texts, ["កម្ពស់", "កំពស់"])

    dob_parts = []

    for idx in [dob_idx, gender_idx, height_idx]:
        if idx >= 0 and texts[idx] not in dob_parts:
            dob_parts.append(texts[idx])

    dob_gender_height = " ".join(dob_parts)

    birth_place = find_first_text(texts, ["ទីកន្លែងកំណើត", "ទូកន្លែងកំណើត"])

    address_1_idx = find_index(
    texts,
    ["អាសយដ្ឋាន", "អាស៊ូយដ្ឋាន", "អាស័យដ្ឋាន", "អាសយជ្ជាន"]
)
    address_1 = texts[address_1_idx] if address_1_idx >= 0 else ""

    address_2 = ""
    if address_1_idx >= 0 and address_1_idx + 1 < len(texts):
        candidate = texts[address_1_idx + 1]

        if not any(k in candidate for k in ["សុពលភាព", "ភិនភាគ", "តិនភាគ", "IDKHM", "<<"]):
            address_2 = candidate

    validity = find_first_text(texts, ["សុពលភាព"])

    body_mark = find_first_text(texts, ["ភិនភាគ", "តិនភាគ", "ប្រជ្រុយ", "ស្នាម"])

    return {
        "id_number": id_number,
        "name": name,
        "latin_name": latin_name,
        "dob_gender_height": dob_gender_height,
        "birth_place": birth_place,
        "address_1": address_1,
        "address_2": address_2,
        "validity": validity,
        "body_mark": body_mark,
        "mrz_1": get_line_text(mrz_lines, 0),
        "mrz_2": get_line_text(mrz_lines, 1),
        "mrz_3": get_line_text(mrz_lines, 2),
    }


def main():
    if not CARD_IMAGE.exists():
        raise FileNotFoundError(f"Card image not found: {CARD_IMAGE}")

    ocr = OCR(
        model_path=MODEL_PATH,
        device="cpu",
        decode_method="beam",
    )

    full_text, results = ocr.extract_text(str(CARD_IMAGE))
    lines = sorted_results(results)

    print("Detected lines:", len(lines))

    for i, r in enumerate(lines, start=1):
        print(f"{i:02d} | box={r.get('box')} | {r.get('text', '')}")

    normal_lines, mrz_lines = split_mrz_and_top_lines(lines)

    print("\nNormal lines:", len(normal_lines))
    for i, r in enumerate(normal_lines, start=1):
        print(f"N{i:02d} | {get_text(r)}")

    print("\nMRZ lines:", len(mrz_lines))
    for i, r in enumerate(mrz_lines, start=1):
        print(f"M{i:02d} | {get_text(r)}")

    raw = map_normal_lines(normal_lines, mrz_lines)

    clean = {
        "id_number": clean_id_number(raw["id_number"]),
        "name": postprocess_field("name", raw["name"]),
        "latin_name": clean_latin_name(raw["latin_name"]),
        "dob_gender_height": postprocess_field("dob_gender_height", raw["dob_gender_height"]),
        "birth_place": postprocess_field("birth_place", raw["birth_place"]),
        "address_1": postprocess_field("address", raw["address_1"]),
        "address_2": postprocess_field("address", raw["address_2"]),
        "validity": postprocess_field("validity", raw["validity"]),
        "body_mark": postprocess_field("body_mark", raw["body_mark"]),
        "mrz_1": clean_mrz_extra(raw["mrz_1"], "mrz_1"),
        "mrz_2": clean_mrz_extra(raw["mrz_2"], "mrz_2"),
        "mrz_3": clean_mrz_extra(raw["mrz_3"], "mrz_3"),
    }

    dob_line = clean["dob_gender_height"]
    validity_line = clean["validity"]

    dob = extract_date(dob_line)
    if not dob:
        dob = dob_from_mrz2(clean["mrz_2"])

    validity_dates = extract_all_dates(validity_line)

    valid_from = validity_dates[0] if len(validity_dates) >= 1 else ""
    valid_to = validity_dates[1] if len(validity_dates) >= 2 else ""

    if not valid_to:
        valid_to = expiry_from_mrz2(clean["mrz_2"])

    id_number = clean["id_number"]

    # Use top printed ID when good. If weak, fallback to MRZ1.
    if len(id_number) < 8:
        mrz1_digits = clean_id_number(clean["mrz_1"])
        if len(mrz1_digits) >= 8:
            id_number = mrz1_digits[:10]

    result = {
        "name_kh": remove_label(clean["name"], ["គោត្តនាមនិងនាម"]),
        "id_number": id_number,
        "latin_name": clean["latin_name"],
        "dob": dob,
        "gender": extract_gender(dob_line),
        "height": extract_height(dob_line),
        "birth_place": remove_label(clean["birth_place"], ["ទីកន្លែងកំណើត"]),
        "address": " ".join(
            part
            for part in [
                remove_label(clean["address_1"], ["អាសយដ្ឋាន"]),
                clean["address_2"],
            ]
            if part
        ),
        "valid_from": valid_from,
        "valid_to": valid_to,
        "body_mark": clean["body_mark"],
        "mrz": [
            clean["mrz_1"],
            clean["mrz_2"],
            clean["mrz_3"],
        ],
        "debug_raw_lines": raw,
        "debug_clean_lines": clean,
    }

    print("\nJSON RESULT:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    out_json = CARD_IMAGE.with_name(CARD_IMAGE.stem + "_detected_extracted.json")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\nSaved:", out_json)


if __name__ == "__main__":
    main()