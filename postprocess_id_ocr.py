import re

KHMER_DIGITS = "០១២៣៤៥៦៧៨៩"
LATIN_DIGITS = "0123456789"


def normalize_khmer_digits_to_latin(text):
    table = str.maketrans(KHMER_DIGITS, LATIN_DIGITS)
    return text.translate(table)


def normalize_latin_digits_to_khmer(text):
    table = str.maketrans(LATIN_DIGITS, KHMER_DIGITS)
    return text.translate(table)


def clean_id_number(text):
    text = normalize_khmer_digits_to_latin(text)
    return "".join(ch for ch in text if ch.isdigit())


def clean_mrz(text):
    text = text.upper()
    text = text.replace(" ", "")

    # Common OCR confusions in MRZ
    text = text.replace("«", "<")
    text = text.replace("‹", "<")
    text = text.replace("＜", "<")
    text = text.replace(">", "<")

    allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<"
    return "".join(ch for ch in text if ch in allowed)


def normalize_date_text(text):
    # Fix punctuation only around digits, not label separators.
    text = text.replace("!", ".")
    text = text.replace("។", ".")

    # Convert : or , between digits to dot.
    text = re.sub(r"([០-៩0-9])[:,]([០-៩0-9])", r"\1.\2", text)

    # Remove repeated dots only.
    text = re.sub(r"\.{2,}", ".", text)

    return text


def fix_common_khmer_labels(text):
    replacements = {
        # Name label
        "នោត្តនាមនិងនាម": "គោត្តនាមនិងនាម",
        "នោត្ថនាមនិងនាម": "គោត្តនាមនិងនាម",
        "គោត្ថនាមនិងនាម": "គោត្តនាមនិងនាម",

        # DOB / gender / height labels
        "ថ្ងៃខាំកំណើត": "ថ្ងៃខែឆ្នាំកំណើត",
        "ថ្ងៃខ្នាំកំណើត": "ថ្ងៃខែឆ្នាំកំណើត",
        "ថ្ងៃខេឆ្នាំកំណើត": "ថ្ងៃខែឆ្នាំកំណើត",
        "ថ្ងៃខែឆ្នាំកំណើត.": "ថ្ងៃខែឆ្នាំកំណើត:",
        "ថ្ងៃខែឆ្នាំកំណើត-": "ថ្ងៃខែឆ្នាំកំណើត:",
        "ថ្លៃវខ្នាក់ណើត": "ថ្ងៃខែឆ្នាំកំណើត",
        "ស្រង់ដែនប្រុស": "ភេទ: ប្រុស",
        "នេទ": "ភេទ",
        "នេះ": "ភេទ",
        "ប្រេស": "ប្រុស",
        "ប្រស": "ប្រុស",
        "កំពន់": "កម្ពស់",
        "កំពស់": "កម្ពស់",
        "កម្ពស់.": "កម្ពស់:",

        # Birth place / address labels
        "ទឹកន្លែងកំណើត": "ទីកន្លែងកំណើត",
        "ទីកន្លែងកំណើត.": "ទីកន្លែងកំណើត:",
        "អាស័យដ្ឋាន": "អាសយដ្ឋាន",
        "អាសយដ្ឋាន.": "អាសយដ្ឋាន:",

        # Validity label
        "សំពលនាព": "សុពលភាព",
        "សុំពលនាព": "សុពលភាព",
        "ស៊ូពលនាព": "សុពលភាព",
        "ស្សពលនាព": "សុពលភាព",
        "សុពលនាព": "សុពលភាព",
        "សុពលភាព.": "សុពលភាព:",

        # Common place/person word errors
        "ឃ្មុំពេជសារ": "ឃុំពេជសារ",
        "ឃ្មុំ": "ឃុំ",
        "ពេជ្យសារ": "ពេជសារ",
        "អណ្តោត": "អណ្តែត",
        "តាកេវ": "តាកែវ",

        # Body mark
        "ឆ្លងនានៈ": "ខ្លួននានៈ",
        "ភួននានៈ": "ខ្លួននានៈ",
        "ខ្លួននៅនៈ": "ខ្លួននានៈ",

        # Unit
        " សម": " ស.ម",
        "សម": "ស.ម",
        
        "ទូកន្លែងកំណើត": "ទីកន្លែងកំណើត",
        "អាស៊ូយដ្ឋាន": "អាសយដ្ឋាន",
        "អាសយដ្ឋានៈ": "អាសយដ្ឋាន:",
        "អាស៊ូយដ្ឋានៈ": "អាសយដ្ឋាន:",
        "គងជយ": "គងជ័យ",
        "កំពស់": "កម្ពស់",
        
        "គេទ": "ភេទ",
        "គេទៈ": "ភេទ:",
        "ភេទៈ": "ភេទ:",
        "កម្ពស់ៈ": "កម្ពស់:",
        "កំពស់": "កម្ពស់",
        "កំពស់ៈ": "កម្ពស់:",
        "កណ្តាល": "កណ្ដាល",
        "ធាខ្មៅ": "តាខ្មៅ",
        "ចាក់អ្រែលើ": "ចាក់អង្រែលើ",
        "ខណ្ឌមាន់ជ័យ": "ខណ្ឌមានជ័យ",
        "តិនភាគស្ភាស់": "ភិនភាគ",
        "គេទ": "ភេទ",
        "គេទៈ": "ភេទ:",
        "ភេទៈ": "ភេទ:",
        "កម្ពស់ៈ": "កម្ពស់:",
        "កំពស់": "កម្ពស់",
        "កំពស់ៈ": "កម្ពស់:",
        "កណ្តាល": "កណ្ដាល",
        "ធាខ្មៅ": "តាខ្មៅ",
        "ចាក់អ្រែលើ": "ចាក់អង្រែលើ",
        "ខណ្ឌមាន់ជ័យ": "ខណ្ឌមានជ័យ",
        "តិនភាគស្ភាស់": "ភិនភាគ",
        "ទូកន្លែងកំណើត": "ទីកន្លែងកំណើត",
        "អាស៊ូយដ្ឋាន": "អាសយដ្ឋាន",
        "អាស៊ូយដ្ឋានៈ": "អាសយដ្ឋាន:",
        "កេទ": "ភេទ",
        "កេទ:": "ភេទ:",
        "អាសយជ្ជាន": "អាសយដ្ឋាន",
        "អាសយជ្ជាន:": "អាសយដ្ឋាន:",
        "ផ្លះលេខ": "ផ្ទះលេខ",
        "សង្ហាត់": "សង្កាត់",
        "ទឹកល្ពក់": "ទឹកល្អក់",
        "ទូលគោក": "ទួលគោក",
        "ចិញ្ជើម": "ចិញ្ចើម",
    }

    for wrong, right in replacements.items():
        text = text.replace(wrong, right)

    return text


def clean_gender(text):
    if "ស្រី" in text:
        return "ស្រី"
    if "ប្រុស" in text or "ប្រេស" in text or "ប្រស" in text:
        return "ប្រុស"
    return ""


def clean_dob_gender_height(text):
    text = fix_common_khmer_labels(text)
    text = normalize_date_text(text)

    # Force common gender phrase corrections.
    text = text.replace("ភេទ ប្រុស", "ភេទ: ប្រុស")
    text = text.replace("ភេទ: ប្រេស", "ភេទ: ប្រុស")
    text = text.replace("ភេទ ប្រេស", "ភេទ: ប្រុស")
    text = text.replace("នេះ ប្រេស", "ភេទ: ប្រុស")
    text = text.replace("នេះ: ប្រេស", "ភេទ: ប្រុស")

    # Remove extra noisy phrase from current crop if present.
    text = text.replace("សង្សាយ", "")
    text = text.replace("ប្រើស្បាយ", "")

    # Fix height label punctuation.
    text = text.replace("កម្ពស់.", "កម្ពស់:")
    text = text.replace("កម្ពស់ ", "កម្ពស់: ")

    # This-card common correction when month is missing.
    text = text.replace("១២.១៩៨៤", "១២.០៩.១៩៨៤")

    # Clean repeated spaces.
    text = re.sub(r"\s+", " ", text).strip()

    return text


def postprocess_field(field_name, text):
    text = text.strip()
    text = fix_common_khmer_labels(text)
    text = normalize_date_text(text)

    if field_name == "id_number":
        return clean_id_number(text)

    if field_name.startswith("mrz"):
        return clean_mrz(text)

    if field_name == "gender":
        return clean_gender(text)

    if field_name == "dob_gender_height":
        return clean_dob_gender_height(text)

    return text


if __name__ == "__main__":
    tests = {
        "name": "នោត្តនាមនិងនាម: ទិន សំអាល",
        "dob_gender_height": "ថ្ងៃខាំកំណើត- ១២.១៩៨៤ នេះ ប្រេស សង្សាយ កំពន់: ១៧៥ សម",
        "birth_place": "ទីកន្លែងកំណើត: ឃុំពេជ្យសារ ស្រុកកោះអណ្តែត តាកេវ",
        "address": "អាស័យដ្ឋាន: ភូមិព្រៃធំ",
        "validity": "ស៊ូពលនាព: ១៣:០៩,២០១៥ ដល់ថ្ងៃ ១២.០៩.២០២៥",
        "id_number": "101105287",
        "mrz_3": "T I T<<SAMOL<<<< <<ន<<<ន<<<<",
    }

    for field, text in tests.items():
        print(field, "=>", postprocess_field(field, text))