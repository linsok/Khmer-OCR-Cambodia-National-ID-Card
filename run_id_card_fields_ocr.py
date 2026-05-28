from pathlib import Path
from kiri_ocr import OCR

# Folder that contains your cropped ID card fields
FIELDS_DIR = Path(r"D:\kiri-ocr-test\my_id_fields_exact")

# Best fine-tuned model
BEST_MODEL = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v3\model.safetensors"

FIELD_ORDER = [
    "id_number_top.jpg",
    "khmer_name.jpg",
    "latin_name.jpg",
    "birth_gender.jpg",
    "birth_place.jpg",
    "address_line_1.jpg",
    "address_line_2.jpg",
    "validity_line.jpg",
    "physical_marks.jpg",
    "mrz_line_1.jpg",
    "mrz_line_2.jpg",
    "mrz_line_3.jpg",
]

FIELD_NAMES = {
    "id_number_top.jpg": "id_number_top",
    "khmer_name.jpg": "khmer_name",
    "latin_name.jpg": "latin_name",
    "birth_gender.jpg": "birth_gender_height",
    "birth_place.jpg": "birth_place",
    "address_line_1.jpg": "address_line_1",
    "address_line_2.jpg": "address_line_2",
    "validity_line.jpg": "validity",
    "physical_marks.jpg": "physical_marks",
    "mrz_line_1.jpg": "mrz_line_1",
    "mrz_line_2.jpg": "mrz_line_2",
    "mrz_line_3.jpg": "mrz_line_3",
}


def clean_common(text: str) -> str:
    """
    General Khmer OCR post-processing.
    These rules fix common OCR mistakes found during Khmer ID testing.
    """

    replacements = {
        # Common Khmer field fixes
        "កំណេើត": "កំណើត",
        "កិណើត": "កំណើត",
        "ទឹកនែង": "ទីកន្លែង",
        "អាសយដាន": "អាសយដ្ឋាន",
        "ផ្លវ": "ផ្លូវ",
        "ភូម១": "ភូមិ",
        "ភមិ": "ភូមិ",
        "ថ្ងែ": "ថ្ងៃ",
        "ថៃ": "ថ្ងៃ",
        "ភ្នពេញ": "ភ្នំពេញ",
        "សង្កាត": "សង្កាត់",
        "សង្កាត់់": "សង្កាត់",
        "បងកក": "បឹងកក់",
        "ទ១": "ទី១",
        "កំពស់": "កម្ពស់",
        "នេទ": "ភេទ",

        # Physical marks field fixes
        "ភនភាគ": "ភិនភាគ",
        "ទននាន": "ភិនភាគ",
        "ប្រជ្រុយច.": "ប្រជ្រុយចំ.",
        "លេចញ្ចេម": "លើចិញ្ចើម",
        "ចញ្ចេម": "ចិញ្ចើម",
        "ខាងឆេង": "ខាងឆ្វេង",
    }

    for wrong, right in replacements.items():
        text = text.replace(wrong, right)

    return " ".join(text.split())


def clean_id_number(text: str) -> str:
    """
    Keep only numbers, Khmer numbers, parentheses, and spaces.
    Useful for the top card ID number.
    """

    allowed = "0123456789០១២៣៤៥៦៧៨៩() "
    cleaned = "".join(ch for ch in text if ch in allowed)
    return " ".join(cleaned.split())


def clean_mrz(text: str) -> str:
    """
    MRZ fields should contain only uppercase Latin letters, numbers, and <.
    Do not blindly replace O with 0 everywhere because country codes use letters.
    """

    allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<"

    text = text.upper()
    text = text.replace(" ", "")
    text = text.replace("«", "<")
    text = text.replace("‹", "<")
    text = text.replace("＜", "<")
    text = text.replace(">", "<")

    return "".join(ch for ch in text if ch in allowed)


def parse_mrz_name(mrz_line_3: str) -> str:
    """
    Convert MRZ name line into readable Latin name.

    Example:
    TIT<<SAMOL<<<<<<<<<<<<<<<<<<<
    becomes:
    TIT SAMOL
    """

    clean = clean_mrz(mrz_line_3)
    name_part = clean.replace("<", " ").strip()
    return " ".join(name_part.split())


def parse_mrz_document_number(mrz_line_1: str) -> str:
    """
    Example:
    IDKHM1011052875<<<<<<<<
    returns:
    1011052875
    """

    line = clean_mrz(mrz_line_1)

    if line.startswith("IDKHM"):
        doc_part = line[5:]
    elif line.startswith("KHM"):
        doc_part = line[3:]
    else:
        doc_part = line

    doc_part = doc_part.split("<")[0]

    # In document number area, OCR often confuses O/I with 0/1.
    doc_part = doc_part.replace("O", "0")
    doc_part = doc_part.replace("I", "1")

    return doc_part


def parse_mrz_birth_expiry(mrz_line_2: str) -> dict:
    """
    Example:
    8409126M2509127KHM<<<<
    birth date = 840912
    sex = M
    expiry = 250912
    nationality = KHM
    """

    line = clean_mrz(mrz_line_2)

    result = {
        "birth_date_yymmdd": "",
        "sex": "",
        "expiry_date_yymmdd": "",
        "nationality": "",
    }

    # ID-1 MRZ commonly follows:
    # YYMMDD + check digit + sex + YYMMDD + check digit + nationality
    if len(line) >= 6:
        result["birth_date_yymmdd"] = line[0:6]

    if len(line) >= 8:
        result["sex"] = line[7]

    if len(line) >= 14:
        result["expiry_date_yymmdd"] = line[8:14]

    if len(line) >= 18:
        result["nationality"] = line[15:18]

    return result


def yymmdd_to_display_date(yymmdd: str, kind: str = "birth") -> str:
    """
    Convert YYMMDD into DD.MM.YYYY.
    For birth dates, assume 1900s if YY looks older.
    For expiry dates, assume 2000s.
    """

    if len(yymmdd) != 6 or not yymmdd.isdigit():
        return ""

    yy = int(yymmdd[0:2])
    mm = yymmdd[2:4]
    dd = yymmdd[4:6]

    if kind == "expiry":
        yyyy = 2000 + yy
    else:
        # Simple rule for Cambodian ID birth dates in current use
        yyyy = 1900 + yy if yy > 30 else 2000 + yy

    return f"{dd}.{mm}.{yyyy}"


def postprocess(field_name: str, text: str) -> str:
    """
    Apply field-specific cleaning.
    """

    text = text.strip()

    if field_name == "id_number_top":
        return clean_id_number(text)

    if field_name.startswith("mrz_line"):
        return clean_mrz(text)

    return clean_common(text)


def main():
    print("Loading best fine-tuned Khmer ID OCR model...")

    ocr = OCR(
        model_path=BEST_MODEL,
        device="cpu",
        decode_method="ctc",
        verbose=False,
    )

    print("\n================ ID CARD OCR RESULTS ================\n")

    final_results = {}

    for filename in FIELD_ORDER:
        img_path = FIELDS_DIR / filename

        if not img_path.exists():
            print(filename, "=> missing")
            continue

        field_name = FIELD_NAMES[filename]

        text, results = ocr.extract_text(str(img_path))
        raw_text = text.strip()
        clean_text = postprocess(field_name, raw_text)

        final_results[field_name] = clean_text

        print(f"{field_name}:")
        print("RAW:  ", raw_text if raw_text else "[EMPTY]")
        print("CLEAN:", clean_text if clean_text else "[EMPTY]")

        for item in results:
            print(
                "  confidence:",
                round(float(item.get("confidence", 0)), 4),
                "| det:",
                round(float(item.get("det_confidence", 0)), 4),
            )

        print("-" * 60)

    # Use MRZ line 3 to get better Latin name
    if "mrz_line_3" in final_results:
        final_results["latin_name_from_mrz"] = parse_mrz_name(
            final_results["mrz_line_3"]
        )

    # Use MRZ line 1 to get better ID number
    if "mrz_line_1" in final_results:
        final_results["id_number_from_mrz"] = parse_mrz_document_number(
            final_results["mrz_line_1"]
        )

    # Use MRZ line 2 to get birth date, sex, expiry, nationality
    if "mrz_line_2" in final_results:
        mrz_info = parse_mrz_birth_expiry(final_results["mrz_line_2"])

        final_results["birth_date_from_mrz_yymmdd"] = mrz_info["birth_date_yymmdd"]
        final_results["birth_date_from_mrz"] = yymmdd_to_display_date(
            mrz_info["birth_date_yymmdd"], kind="birth"
        )

        final_results["sex_from_mrz"] = mrz_info["sex"]

        final_results["expiry_date_from_mrz_yymmdd"] = mrz_info["expiry_date_yymmdd"]
        final_results["expiry_date_from_mrz"] = yymmdd_to_display_date(
            mrz_info["expiry_date_yymmdd"], kind="expiry"
        )

        final_results["nationality_from_mrz"] = mrz_info["nationality"]

    print("\n================ FINAL STRUCTURED OUTPUT ================\n")

    for key, value in final_results.items():
        print(f"{key}: {value}")
        
        
    print("\n================ TRUSTED OUTPUT ================\n")

    trusted = {
        "id_number": final_results.get("id_number_from_mrz", "") or final_results.get("id_number_top", ""),
        "latin_name": final_results.get("latin_name_from_mrz", "") or final_results.get("latin_name", ""),
        "birth_date": final_results.get("birth_date_from_mrz", ""),
        "sex": final_results.get("sex_from_mrz", ""),
        "expiry_date": final_results.get("expiry_date_from_mrz", ""),
        "nationality": final_results.get("nationality_from_mrz", ""),
        "khmer_name_raw": final_results.get("khmer_name", ""),
        "birth_place_raw": final_results.get("birth_place", ""),
        "address_line_1_raw": final_results.get("address_line_1", ""),
        "address_line_2_raw": final_results.get("address_line_2", ""),
        "validity_raw": final_results.get("validity", ""),
        "physical_marks_raw": final_results.get("physical_marks", ""),
    }

    for key, value in trusted.items():
        print(f"{key}: {value}")
        


if __name__ == "__main__":
    main()