import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUT_DIR = Path("data/khmer_real_id_errorfix_v1")
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

random.seed(3030)

KHMER_FONTS = [
    r"C:\Windows\Fonts\khmerui.ttf",
    r"C:\Windows\Fonts\KhmerUI.ttf",
    r"C:\Windows\Fonts\NotoSansKhmer-Regular.ttf",
]

LATIN_FONTS = [
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\consola.ttf",
    r"C:\Windows\Fonts\cour.ttf",
]

def find_font(candidates):
    for p in candidates:
        if Path(p).exists():
            return p
    raise FileNotFoundError("Font not found")

KHMER_FONT = find_font(KHMER_FONTS)
LATIN_FONT = find_font(LATIN_FONTS)

print("Using Khmer font:", KHMER_FONT)
print("Using Latin font:", LATIN_FONT)

khmer_digits_map = str.maketrans("0123456789", "០១២៣៤៥៦៧៨៩")

def khmer_digits(s):
    return str(s).translate(khmer_digits_map)

khmer_names = [
    "ទិន សំអុល",
    "ទិត សំអុល",
    "សុខ សុវណ្ណ",
    "ចាន់ សុភ័ក្រ",
    "ហេង សំណាង",
    "លី សុភា",
    "ស្រី ច័ន្ទ",
]

latin_names = [
    "TIT SAMOL",
    "TIN SAMOL",
    "SOK SOVANN",
    "CHAN SOPHEAK",
    "HENG SAMNANG",
    "LY SOPHEA",
]

dob_lines = [
    "ថ្ងៃខែឆ្នាំកំណើត: ១២.០៩.១៩៨៤ ភេទ: ប្រុស កម្ពស់: ១៧៥ ស.ម",
    "ថ្ងៃខែឆ្នាំកំណើត: ០៦.១០.១៩៧៣ ភេទ: ប្រុស កម្ពស់: ១៧០ ស.ម",
    "ថ្ងៃខែឆ្នាំកំណើត: ២៨.០៨.១៩៩៧ ភេទ: ស្រី កម្ពស់: ១៦៥ ស.ម",
    "ថ្ងៃខែឆ្នាំកំណើត: ១៤.០២.១៩៧៦ ភេទ: ប្រុស កម្ពស់: ១៥៥ ស.ម",
    "ថ្ងៃខែឆ្នាំកំណើត: ០១.០១.១៩៩៩ ភេទ: ស្រី កម្ពស់: ១៦០ ស.ម",
]

birth_places = [
    "ទីកន្លែងកំណើត: ឃុំពេជសារ ស្រុកកោះអណ្តែត តាកែវ",
    "ទីកន្លែងកំណើត: ឃុំគគីរ ស្រុកកៀនស្វាយ កណ្ដាល",
    "ទីកន្លែងកំណើត: ឃុំស្វាយរំពារ ស្រុកស្វាយជ្រំ ស្វាយរៀង",
    "ទីកន្លែងកំណើត: សង្កាត់ទន្លេបាសាក់ ខណ្ឌចំការមន ភ្នំពេញ",
]

addresses = [
    "អាសយដ្ឋាន: ភូមិព្រៃធំ",
    "អាសយដ្ឋាន: ភូមិជ្រោយ",
    "អាសយដ្ឋាន: ភូមិកណ្ដាល",
    "ឃុំពេជសារ ស្រុកកោះអណ្តែត តាកែវ",
    "ឃុំគគីរ ស្រុកកៀនស្វាយ កណ្ដាល",
    "សង្កាត់ទឹកថ្លា ខណ្ឌសែនសុខ ភ្នំពេញ",
]

validity_lines = [
    "សុពលភាព: ១៣.០៩.២០១៥ ដល់ថ្ងៃ ១២.០៩.២០២៥",
    "សុពលភាព: ០១.០១.២០២០ ដល់ថ្ងៃ ០១.០១.២០៣០",
    "សុពលភាព: ២៥.១២.២០១៩ ដល់ថ្ងៃ ២៥.១២.២០២៩",
    "សុពលភាព: ១០.០៥.២០១៨ ដល់ថ្ងៃ ១០.០៥.២០២៨",
]

body_marks = [
    "ខ្លួននានៈ សំលាកតូចចំ ០,៥សម ក្រោយចុងចិញ្ចើមឆ្វេង",
    "ខ្លួននានៈ សំលាកតូចចំ ០,៥សម ក្រោយក្រោមចុងចិញ្ចើមឆ្វេង",
    "ខ្លួននានៈ ស្នាមតូច ០,៥សម នៅថ្ពាល់ស្តាំ",
]

id_numbers = [
    "1011105287",
    "1011052875",
    "1234567890",
    "9876543210",
    "8409126250",
]

mrz_lines = [
    "IDKHM1011052875<<<<<<<<<<<<<<<",
    "IDKHM1011105287<<<<<<<<<<<<<<<",
    "8409126M2509127KHM<<<<<<<<<<<<",
    "8409126M25091227KHM<<<<<<<<<<<",
    "TIT<<SAMOL<<<<<<<<<<<<<<<<<<<<",
    "TIN<<SAMOL<<<<<<<<<<<<<<<<<<<<",
    "SOK<<SOVANN<<<<<<<<<<<<<<<<<<",
]

def sample():
    r = random.random()
    if r < 0.12:
        return "គោត្តនាមនិងនាម: " + random.choice(khmer_names), "khmer"
    if r < 0.24:
        return random.choice(dob_lines), "khmer"
    if r < 0.36:
        return random.choice(birth_places), "khmer"
    if r < 0.48:
        return random.choice(addresses), "khmer"
    if r < 0.60:
        return random.choice(validity_lines), "khmer"
    if r < 0.70:
        return random.choice(body_marks), "khmer"
    if r < 0.78:
        return random.choice(khmer_names), "khmer"
    if r < 0.85:
        return random.choice(latin_names), "latin"
    if r < 0.92:
        return random.choice(id_numbers), "latin"
    return random.choice(mrz_lines), "mrz"

def add_noise(img):
    # Real card style: moderate blur / contrast / background
    if random.random() < 0.35:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.05, 0.35)))
    if random.random() < 0.25:
        img = img.rotate(random.uniform(-0.5, 0.5), expand=True, fillcolor=(240, 245, 232))
    if random.random() < 0.35:
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.85, 1.20))
    if random.random() < 0.35:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.88, 1.10))
    return img

def render(text, kind, filename):
    if kind == "mrz":
        font_path = LATIN_FONT
        font_size = random.choice([26, 28, 30, 32])
        width = 720
        height = random.choice([48, 52, 56])
    elif kind == "latin":
        font_path = LATIN_FONT
        font_size = random.choice([22, 24, 26, 28])
        width = max(230, min(700, 90 + len(text) * 18))
        height = random.choice([44, 48, 52])
    else:
        font_path = KHMER_FONT
        font_size = random.choice([22, 24, 26, 28])
        width = max(300, min(1150, 120 + len(text) * 18))
        height = random.choice([52, 56, 60, 64])

    img = Image.new("RGB", (width, height), random.choice([
        (245, 248, 238),
        (238, 246, 230),
        (250, 250, 240),
        (240, 245, 232),
    ]))

    draw = ImageDraw.Draw(img)

    # ID-card-like faint background lines
    if random.random() < 0.45:
        for y in range(0, height, random.randint(12, 18)):
            draw.line((0, y, width, y), fill=(224, 230, 218), width=1)
    if random.random() < 0.25:
        for x in range(0, width, random.randint(24, 38)):
            draw.line((x, 0, x, height), fill=(230, 235, 220), width=1)

    font = ImageFont.truetype(font_path, font_size)
    x = random.randint(8, 16)
    y = random.randint(7, 14)

    draw.text((x, y), text, font=font, fill=random.choice([(8, 8, 8), (30, 30, 30), (55, 55, 55)]))

    img = add_noise(img)
    img.save(IMG_DIR / filename, quality=95)

def create_dataset(n=8000):
    rows = []
    for i in range(1, n + 1):
        text, kind = sample()
        filename = f"realid_errorfix_{i:06d}.jpg"
        render(text, kind, filename)
        rows.append(f"images/{filename}\t{text}")

    random.shuffle(rows)

    val_count = int(len(rows) * 0.1)
    val_rows = rows[:val_count]
    train_rows = rows[val_count:]

    with open(OUT_DIR / "train_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(train_rows))

    with open(OUT_DIR / "val_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(val_rows))

    print("Done generating real ID error-fix dataset")
    print("Output folder:", OUT_DIR)
    print("Total:", len(rows))
    print("Train:", len(train_rows))
    print("Val:", len(val_rows))
    print("Example:", rows[0])

if __name__ == "__main__":
    create_dataset(n=8000)