import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUT_DIR = Path("data/khmer_real_id_style_v1")
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

random.seed(2027)

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

khmer_first = ["ទិត", "សុខ", "ចាន់", "ហេង", "លី", "ពៅ", "ស្រី", "មុនី", "វិសាល", "ដារ៉ា", "រតនា"]
khmer_last = ["សំអុល", "សំអុង", "សុវណ្ណ", "សុភ័ក្រ", "វណ្ណា", "ច័ន្ទ", "ពិសី", "រដ្ឋា", "សំណាង"]

latin_first = ["TIT", "SOK", "CHAN", "HENG", "LY", "POV", "SREY", "MONY", "VISAL", "DARA"]
latin_last = ["SAMOL", "SAMONG", "SOVANN", "SOPHEAK", "VANNA", "CHANT", "PICH", "SAMNANG"]

villages = ["ភូមិព្រៃធំ", "ភូមិជ្រោយ", "ភូមិកណ្ដាល", "ភូមិសាមគ្គី", "ភូមិថ្មី", "ភូមិព្រែក"]
communes = ["ឃុំពេជសារ", "ឃុំគគីរ", "ឃុំស្វាយរំពារ", "ឃុំព្រែកអញ្ចាញ", "សង្កាត់ទន្លេបាសាក់", "សង្កាត់ទឹកថ្លា"]
districts = ["ស្រុកកោះអណ្តែត", "ស្រុកបាទី", "ស្រុកកៀនស្វាយ", "ស្រុកស្វាយជ្រំ", "ខណ្ឌសែនសុខ", "ខណ្ឌចំការមន"]
provinces = ["តាកែវ", "កណ្ដាល", "កំពត", "ភ្នំពេញ", "កំពង់ចាម", "បាត់ដំបង", "សៀមរាប"]

khmer_digits_map = str.maketrans("0123456789", "០១២៣៤៥៦៧៨៩")

def khmer_digits(s):
    return str(s).translate(khmer_digits_map)

def rand_id():
    return "".join(random.choice("0123456789") for _ in range(10))

def rand_khmer_date(y1=1960, y2=2035):
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(y1, y2)
    return khmer_digits(f"{d:02d}.{m:02d}.{y}")

def rand_latin_date_yy(y1=1960, y2=2005):
    y = random.randint(y1, y2)
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    return f"{str(y)[-2:]}{m:02d}{d:02d}"

def rand_khmer_name():
    return random.choice(khmer_first) + " " + random.choice(khmer_last)

def rand_latin_name():
    return random.choice(latin_first) + " " + random.choice(latin_last)

def rand_gender():
    return random.choice(["ប្រុស", "ស្រី"])

def rand_height():
    return khmer_digits(str(random.choice([155, 160, 165, 168, 170, 172, 175, 178]))) + " ស.ម"

def rand_place():
    return random.choice(communes) + " " + random.choice(districts) + " " + random.choice(provinces)

def rand_address():
    return random.choice(villages) + " " + random.choice(communes) + " " + random.choice(districts) + " " + random.choice(provinces)

def rand_body_mark():
    return random.choice([
        "ខ្លួននៅនៈ សំលាកតូចចំ ០,៥សម នៅក្រោយចុងចិញ្ចើមឆ្វេង",
        "ខ្លួននៅនៈ ស្នាមតូច ០,៥សម នៅថ្ពាល់ស្តាំ",
        "ខ្លួននៅនៈ ស្នាមតូច នៅក្រោមភ្នែកឆ្វេង",
    ])

def mrz_lines(id_num, latin_name):
    name_parts = latin_name.split()
    first = name_parts[0]
    last = name_parts[-1]

    dob = rand_latin_date_yy(1960, 2005)
    exp = rand_latin_date_yy(2026, 2035)
    sex = random.choice(["M", "F"])

    line1 = ("IDKHM" + id_num + "5" + "<" * 30)[:30]
    line2 = (dob + sex + exp + "KHM" + "<" * 20)[:30]
    line3 = (first + "<<" + last + "<" * 30)[:30]
    return line1, line2, line3

def build_fields():
    id_num = rand_id()
    kh_name = rand_khmer_name()
    en_name = rand_latin_name()

    dob = rand_khmer_date(1960, 2005)
    issue = rand_khmer_date(2010, 2024)
    expiry = rand_khmer_date(2025, 2035)

    line1, line2, line3 = mrz_lines(id_num, en_name)

    fields = [
        ("គោត្តនាមនិងនាមៈ " + kh_name, "khmer"),
        (id_num, "latin"),
        ("ថ្ងៃខែឆ្នាំកំណើត: " + dob + " ភេទ: " + rand_gender() + " កម្ពស់: " + rand_height(), "khmer"),
        (en_name, "latin"),
        ("ទីកន្លែងកំណើត: " + rand_place(), "khmer"),
        ("អាសយដ្ឋាន: " + rand_address(), "khmer"),
        (rand_address(), "khmer"),
        (rand_body_mark(), "khmer"),
        ("សុពលភាព: " + issue + " ដល់ថ្ងៃ " + expiry, "khmer"),
        (line1, "mrz"),
        (line2, "mrz"),
        (line3, "mrz"),

        # raw values too, because detector may crop only value
        (kh_name, "khmer"),
        (en_name, "latin"),
        (khmer_digits(id_num), "khmer"),
        (dob, "khmer"),
        (issue + " ដល់ថ្ងៃ " + expiry, "khmer"),
    ]

    return fields

def add_noise(img):
    if random.random() < 0.35:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.05, 0.35)))

    if random.random() < 0.25:
        angle = random.uniform(-0.5, 0.5)
        img = img.rotate(angle, expand=True, fillcolor=(240, 245, 232))

    if random.random() < 0.35:
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.85, 1.25))

    if random.random() < 0.35:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.88, 1.12))

    return img

def draw_bg(draw, width, height):
    if random.random() < 0.55:
        for y in range(0, height, random.randint(12, 18)):
            draw.line((0, y, width, y), fill=(222, 230, 214), width=1)
    if random.random() < 0.35:
        for x in range(0, width, random.randint(22, 35)):
            draw.line((x, 0, x, height), fill=(230, 235, 220), width=1)

def render(text, filename, kind):
    if kind == "mrz":
        width = 660
        height = random.choice([42, 46, 50])
        font_path = LATIN_FONT
        font_size = random.choice([27, 29, 31])
    elif kind == "latin":
        width = max(220, min(680, 80 + len(text) * 17))
        height = random.choice([42, 46, 50])
        font_path = LATIN_FONT
        font_size = random.choice([22, 24, 26])
    else:
        width = max(260, min(1050, 100 + len(text) * 18))
        height = random.choice([50, 54, 58, 62])
        font_path = KHMER_FONT
        font_size = random.choice([22, 24, 26, 28])

    img = Image.new("RGB", (width, height), random.choice([
        (245, 248, 238),
        (238, 246, 230),
        (250, 250, 240),
        (240, 245, 232),
    ]))

    draw = ImageDraw.Draw(img)
    draw_bg(draw, width, height)

    font = ImageFont.truetype(font_path, font_size)
    x = random.randint(7, 15)
    y = random.randint(6, 13)

    draw.text((x, y), text, font=font, fill=random.choice([(8, 8, 8), (30, 30, 30), (55, 55, 55)]))

    img = add_noise(img)
    img.save(IMG_DIR / filename, quality=random.choice([90, 95]))

def create_dataset(records=1000):
    rows = []
    idx = 0

    for _ in range(records):
        for text, kind in build_fields():
            idx += 1
            filename = f"realidstyle_{idx:06d}.jpg"
            render(text, filename, kind)
            rows.append(f"images/{filename}\t{text}")

    random.shuffle(rows)
    val_count = int(len(rows) * 0.1)

    val_rows = rows[:val_count]
    train_rows = rows[val_count:]

    with open(OUT_DIR / "train_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(train_rows))

    with open(OUT_DIR / "val_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(val_rows))

    print("Done generating real-ID-style synthetic crops")
    print("Output folder:", OUT_DIR)
    print("Total images:", len(rows))
    print("Train:", len(train_rows))
    print("Val:", len(val_rows))
    print("Example:")
    print(rows[0])

if __name__ == "__main__":
    create_dataset(records=1000)