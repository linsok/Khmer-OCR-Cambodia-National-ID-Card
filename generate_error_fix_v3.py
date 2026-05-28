import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUT_DIR = Path("data/khmer_error_fix_v3")
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

random.seed(2026)

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\khmerui.ttf",
    r"C:\Windows\Fonts\KhmerUI.ttf",
    r"C:\Windows\Fonts\NotoSansKhmer-Regular.ttf",
]

def find_font():
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return p
    raise FileNotFoundError("No Khmer font found.")

FONT_PATH = find_font()
print("Using font:", FONT_PATH)

khmer_digits_map = str.maketrans("0123456789", "០១២៣៤៥៦៧៨៩")

def khmer_digits(s):
    return str(s).translate(khmer_digits_map)

# Exact remaining difficult labels from v8 beam errors
exact_hard_cases = [
    "ភូមិជ្រោយ សង្កាត់ទន្លេបាសាក់ ស្រុកស្វាយជ្រំ កំពត",
    "ស្រុកបាទី កំពត",
    "ភូមិកណ្ដាល ឃុំត្រពាំងក្រសាំង ស្រុកស្វាយជ្រំ បាត់ដំបង",
    "ភូមិជ្រោយ ឃុំស្វាយរំពារ ខណ្ឌសែនសុខ ភ្នំពេញ",
    "ខ្មែរ",
    "៧៦៤៧៧០៩០៦",
    "កញ្ញា សំណាង",
    "ភូមិសាមគ្គី ឃុំស្វាយរំពារ ស្រុកស្រីសន្ធរ កណ្ដាល",
    "ភូមិសាមគ្គី ឃុំព្រែកអញ្ចាញ ស្រុកស្រីសន្ធរ កំពត",
    "ខណ្ឌសែនសុខ សៀមរាប",
    "ភូមិសាមគ្គី សង្កាត់ទន្លេបាសាក់ ស្រុកអង្គស្នួល បាត់ដំបង",
    "ភូមិថ្មី ឃុំស្វាយរំពារ ស្រុកស្វាយជ្រំ សៀមរាប",
    "ភូមិកណ្ដាល សង្កាត់ទឹកថ្លា ខណ្ឌចំការមន កំពង់ចាម",
    "ភូមិកណ្ដាល សង្កាត់ទន្លេបាសាក់ ស្រុកស្វាយជ្រំ កណ្ដាល",
    "ភូមិជ្រោយ ឃុំព្រែកអញ្ចាញ ស្រុកអង្គស្នួល ស្វាយរៀង",
    "ភូមិព្រែក សង្កាត់ទន្លេបាសាក់ ស្រុកស្រីសន្ធរ ភ្នំពេញ",
    "០៦.១០.១៩៧៣",
    "ភូមិជ្រោយ សង្កាត់ទន្លេបាសាក់ ស្រុកស្រីសន្ធរ កំពង់ចាម",
    "ស្រុកអង្គស្នួល កំពង់ចាម",
    "ស្រី ច័ន្ទ",
]

short_hard_words = [
    "ខ្មែរ",
    "កញ្ញា",
    "សំណាង",
    "ស្រី ច័ន្ទ",
    "ស្រុក",
    "ស្រុកបាទី",
    "ស្រុកស្វាយជ្រំ",
    "ស្រុកស្រីសន្ធរ",
    "ស្រុកអង្គស្នួល",
    "ភូមិជ្រោយ",
    "ភូមិកណ្ដាល",
    "ភូមិសាមគ្គី",
    "សង្កាត់ទន្លេបាសាក់",
    "កំពត",
    "កណ្ដាល",
    "ភ្នំពេញ",
    "កំពង់ចាម",
    "បាត់ដំបង",
    "សៀមរាប",
]

date_cases = [
    "០៦.១០.១៩៧៣",
    "២៨.០៨.១៩៩៧",
    "០១.០១.១៩៩៩",
    "០៦.០៦.១៩៨៦",
    "១៦.១០.១៩៧៣",
    "២៥.១២.២០៣០",
]

id_cases = [
    "៧៦៤៧៧០៩០៦",
    "១២៣៤៥៦៧៨៩",
    "៩៤៣៧៥៤៨២៦",
    "០១២៣៤៥៦៧",
    "៥៨៧០៩៦៤៣២",
]

def sample_text():
    r = random.random()
    if r < 0.55:
        return random.choice(exact_hard_cases)
    if r < 0.78:
        return random.choice(short_hard_words)
    if r < 0.90:
        return random.choice(date_cases)
    return random.choice(id_cases)

def add_noise(img):
    # Keep image mostly clean; we are fixing exact character confusion now
    if random.random() < 0.20:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.03, 0.20)))

    if random.random() < 0.18:
        angle = random.uniform(-0.4, 0.4)
        img = img.rotate(angle, expand=True, fillcolor=(245, 245, 235))

    if random.random() < 0.25:
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.95, 1.18))

    if random.random() < 0.25:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.94, 1.08))

    return img

def render_text_crop(text, filename):
    width = max(280, min(1150, 120 + len(text) * 19))
    height = random.choice([54, 58, 62, 66])

    bg = random.choice([
        (245, 248, 238),
        (238, 246, 230),
        (250, 250, 240),
        (240, 245, 232),
    ])

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    font_size = random.choice([24, 25, 26, 27, 28, 30])
    font = ImageFont.truetype(FONT_PATH, font_size)

    if random.random() < 0.30:
        for y in range(0, height, random.randint(13, 20)):
            draw.line((0, y, width, y), fill=(224, 230, 218), width=1)

    x = random.randint(8, 14)
    y = random.randint(8, 14)

    draw.text(
        (x, y),
        text,
        font=font,
        fill=random.choice([(8, 8, 8), (25, 25, 25), (45, 45, 45)])
    )

    img = add_noise(img)
    img.save(IMG_DIR / filename, quality=95)

def create_dataset(n=3000):
    rows = []

    for i in range(1, n + 1):
        text = sample_text()
        filename = f"errorfix_v3_{i:06d}.jpg"
        render_text_crop(text, filename)
        rows.append(f"images/{filename}\t{text}")

    random.shuffle(rows)

    val_count = int(len(rows) * 0.1)
    val_rows = rows[:val_count]
    train_rows = rows[val_count:]

    with open(OUT_DIR / "train_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(train_rows))

    with open(OUT_DIR / "val_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(val_rows))

    print("Done generating targeted error-fix v3 dataset")
    print("Output folder:", OUT_DIR)
    print("Total images:", len(rows))
    print("Train:", len(train_rows))
    print("Val:", len(val_rows))
    print("Example:")
    print(rows[0])

if __name__ == "__main__":
    create_dataset(n=3000)