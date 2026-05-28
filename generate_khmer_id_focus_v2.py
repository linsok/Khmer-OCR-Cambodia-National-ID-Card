import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUT_DIR = Path("data/khmer_id_focus_v2")
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

random.seed(777)

FONT_CANDIDATES_KHMER = [
    r"C:\Windows\Fonts\khmerui.ttf",
    r"C:\Windows\Fonts\KhmerUI.ttf",
    r"C:\Windows\Fonts\NotoSansKhmer-Regular.ttf",
]

FONT_CANDIDATES_LATIN = [
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\consola.ttf",
    r"C:\Windows\Fonts\cour.ttf",
]

def find_font(candidates):
    for p in candidates:
        if Path(p).exists():
            return p
    raise FileNotFoundError("No usable font found")

KHMER_FONT = find_font(FONT_CANDIDATES_KHMER)
LATIN_FONT = find_font(FONT_CANDIDATES_LATIN)

print("Using Khmer font:", KHMER_FONT)
print("Using Latin font:", LATIN_FONT)

khmer_first_names = [
    "ទិត្យ", "សុខ", "ចាន់", "ហេង", "លី", "ពៅ", "ស្រី", "មុនី",
    "វិសាល", "ដារ៉ា", "រតនា", "សុជាតិ", "វណ្ណ", "សុភា"
]

khmer_last_names = [
    "សមុល", "សុវណ្ណ", "សុភ័ក្រ", "វណ្ណា", "សីហា", "ច័ន្ទ",
    "ពិសី", "រដ្ឋា", "មករា", "សុធា", "ធីតា", "សំណាង"
]

latin_first_names = [
    "TIT", "SOK", "CHAN", "HENG", "LY", "POV", "SREY",
    "MONY", "VISAL", "DARA", "RATANA", "VANNA"
]

latin_last_names = [
    "SAMOL", "SOVANN", "SOPHEAK", "SEYHA", "PICH",
    "MAKARA", "SOTHEA", "SAMNANG"
]

provinces = [
    "ភ្នំពេញ", "កណ្ដាល", "បាត់ដំបង", "សៀមរាប", "កំពត",
    "តាកែវ", "ព្រៃវែង", "ស្វាយរៀង", "កំពង់ចាម", "កំពង់ស្ពឺ",
    "កំពង់ធំ", "ពោធិ៍សាត់", "ព្រះសីហនុ"
]

districts = [
    "ស្រុកបាទី", "ស្រុកកៀនស្វាយ", "ស្រុកអង្គស្នួល",
    "ស្រុកស្វាយជ្រំ", "ខណ្ឌសែនសុខ", "ខណ្ឌចំការមន",
    "ខណ្ឌដូនពេញ", "ខណ្ឌមានជ័យ"
]

communes = [
    "ឃុំគគីរ", "ឃុំស្វាយរំពារ", "ឃុំត្រពាំងក្រសាំង",
    "ឃុំព្រែកអញ្ចាញ", "សង្កាត់ទឹកថ្លា",
    "សង្កាត់ទន្លេបាសាក់", "សង្កាត់បឹងកេងកង"
]

villages = [
    "ភូមិថ្មី", "ភូមិកណ្ដាល", "ភូមិព្រែក", "ភូមិជ្រោយ",
    "ភូមិសាមគ្គី", "ភូមិត្រពាំង", "ភូមិបឹង"
]

khmer_digits_map = str.maketrans("0123456789", "០១២៣៤៥៦៧៨៩")

def khmer_digits(s):
    return str(s).translate(khmer_digits_map)

def random_id_latin():
    return "".join(random.choice("0123456789") for _ in range(9))

def random_id_khmer():
    return khmer_digits(random_id_latin())

def random_date_khmer(y1=1960, y2=2040):
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(y1, y2)
    return khmer_digits(f"{d:02d}.{m:02d}.{y}")

def random_date_latin(y1=1960, y2=2040):
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(y1, y2)
    return f"{d:02d}.{m:02d}.{y}"

def random_khmer_name():
    return random.choice(khmer_first_names) + " " + random.choice(khmer_last_names)

def random_latin_name():
    return random.choice(latin_first_names) + " " + random.choice(latin_last_names)

def random_gender():
    return random.choice(["ប្រុស", "ស្រី"])

def random_height():
    return khmer_digits(random.choice(["១៦០", "១៦៥", "១៦៨", "១៧០", "១៧២", "១៧៥"])) + " ស.ម"

def random_birth_place():
    return random.choice(districts) + " " + random.choice(provinces)

def random_address():
    return (
        random.choice(villages) + " " +
        random.choice(communes) + " " +
        random.choice(districts) + " " +
        random.choice(provinces)
    )

def random_mrz_name():
    first = random.choice(latin_first_names)
    last = random.choice(latin_last_names)
    return f"{first}<{last}"

def random_mrz_line_1(id_number):
    return ("IDKHM" + id_number + "<" * 20)[:30]

def random_mrz_line_2():
    yy = random.randint(60, 99)
    mm = random.randint(1, 12)
    dd = random.randint(1, 28)
    exp_y = random.randint(25, 35)
    exp_m = random.randint(1, 12)
    exp_d = random.randint(1, 28)
    sex = random.choice(["M", "F"])
    return f"{yy:02d}{mm:02d}{dd:02d}{sex}{exp_y:02d}{exp_m:02d}{exp_d:02d}KHM" + "<" * 15

def random_mrz_line_3():
    name = random_mrz_name()
    return (name + "<" * 30)[:30]

def add_noise(img):
    if random.random() < 0.45:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.1, 0.45)))

    if random.random() < 0.35:
        angle = random.uniform(-1.2, 1.2)
        img = img.rotate(angle, expand=True, fillcolor=(236, 242, 228))

    if random.random() < 0.40:
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.75, 1.35))

    if random.random() < 0.40:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.82, 1.18))

    return img

def draw_background(draw, width, height):
    if random.random() < 0.65:
        for x in range(0, width, random.randint(16, 28)):
            draw.line((x, 0, x + random.randint(-8, 8), height), fill=(218, 228, 210), width=1)

    if random.random() < 0.65:
        for y in range(0, height, random.randint(10, 18)):
            draw.line((0, y, width, y), fill=(224, 230, 216), width=1)

    if random.random() < 0.35:
        for _ in range(8):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=(210, 225, 205), width=1)

def render_text_crop(text, filename, lang="khmer", style="field"):
    if style == "mrz":
        width = 620
        height = random.choice([44, 48, 52])
        font_path = LATIN_FONT
        font_size = random.choice([28, 30, 32])
        color_choices = [(20, 20, 20), (35, 35, 35)]
    elif lang == "latin":
        width = max(220, min(620, 70 + len(text) * 18))
        height = random.choice([42, 46, 50])
        font_path = LATIN_FONT
        font_size = random.choice([22, 24, 26])
        color_choices = [(20, 20, 20), (40, 40, 40)]
    else:
        width = max(230, min(760, 90 + len(text) * 19))
        height = random.choice([44, 48, 52, 56, 60])
        font_path = KHMER_FONT
        font_size = random.choice([20, 22, 24, 26, 28])
        color_choices = [(10, 10, 10), (30, 30, 30), (50, 50, 50)]

    bg = random.choice([
        (238, 246, 230),
        (232, 242, 226),
        (245, 248, 238),
        (238, 240, 228),
        (248, 248, 240),
    ])

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    draw_background(draw, width, height)

    font = ImageFont.truetype(font_path, font_size)

    x = random.randint(6, 16)
    y = random.randint(4, 12)

    draw.text((x, y), text, font=font, fill=random.choice(color_choices))

    img = add_noise(img)
    img.save(IMG_DIR / filename, quality=random.choice([85, 90, 95]))

def make_record_fields():
    id_number = random_id_latin()
    kh_name = random_khmer_name()
    en_name = random_latin_name()

    fields = []

    # Top right ID number
    fields.append((id_number, "latin", "field"))

    # Name block like sample card
    fields.append(("គោត្តនាមនិងនាម: " + kh_name, "khmer", "field"))
    fields.append((en_name, "latin", "field"))

    # Details line
    fields.append(("ថ្ងៃខែឆ្នាំកំណើត: " + random_date_khmer(1960, 2005), "khmer", "field"))
    fields.append(("ភេទ: " + random_gender(), "khmer", "field"))
    fields.append(("កម្ពស់: " + random_height(), "khmer", "field"))

    # Birth and address lines
    fields.append(("ទីកន្លែងកំណើត: " + random_birth_place(), "khmer", "field"))
    fields.append(("អាសយដ្ឋាន: " + random_address(), "khmer", "field"))

    # Nationality and date fields
    fields.append(("សញ្ជាតិ: ខ្មែរ", "khmer", "field"))
    fields.append(("ផ្តល់នៅ: " + random_date_khmer(2015, 2025), "khmer", "field"))
    fields.append(("ផុតកំណត់: " + random_date_khmer(2026, 2036), "khmer", "field"))

    # MRZ style bottom lines
    fields.append((random_mrz_line_1(id_number), "latin", "mrz"))
    fields.append((random_mrz_line_2(), "latin", "mrz"))
    fields.append((random_mrz_line_3(), "latin", "mrz"))

    # Also add raw values only because OCR crops may not include labels
    fields.append((kh_name, "khmer", "field"))
    fields.append((en_name, "latin", "field"))
    fields.append((khmer_digits(id_number), "khmer", "field"))
    fields.append((random_gender(), "khmer", "field"))
    fields.append(("ខ្មែរ", "khmer", "field"))

    return fields

def create_dataset(num_records=800):
    rows = []
    idx = 0

    for _ in range(num_records):
        for text, lang, style in make_record_fields():
            idx += 1
            filename = f"idcard_struct_{idx:06d}.jpg"
            render_text_crop(text, filename, lang=lang, style=style)
            rows.append(f"images/{filename}\t{text}")

    random.shuffle(rows)

    val_count = max(1, int(len(rows) * 0.1))
    val_rows = rows[:val_count]
    train_rows = rows[val_count:]

    with open(OUT_DIR / "train_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(train_rows))

    with open(OUT_DIR / "val_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(val_rows))

    print("Done generating Khmer ID-card-structure OCR crops")
    print("Output folder:", OUT_DIR)
    print("Total images:", len(rows))
    print("Train:", len(train_rows))
    print("Val:", len(val_rows))
    print("Example:")
    print(rows[0])

if __name__ == "__main__":
    create_dataset(num_records=800)