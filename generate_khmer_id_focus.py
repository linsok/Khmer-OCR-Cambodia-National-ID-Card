import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = Path("data/khmer_id_focus")
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

random.seed(123)

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\khmerui.ttf",
    r"C:\Windows\Fonts\KhmerUI.ttf",
    r"C:\Windows\Fonts\NotoSansKhmer-Regular.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]

def find_font():
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return p
    raise FileNotFoundError("No Khmer font found. Install Khmer UI or Noto Sans Khmer.")

FONT_PATH = find_font()
print("Using font:", FONT_PATH)

# Weak words from your test
short_fields = [
    "ខ្មែរ",
    "ស្រី",
    "ប្រុស",
    "សញ្ជាតិ ខ្មែរ",
    "ភេទ ស្រី",
    "ភេទ ប្រុស",
]

places = [
    "ស្រុកបាទី",
    "កណ្ដាល",
    "បាត់ដំបង",
    "កំពត",
    "ភ្នំពេញ",
    "សៀមរាប",
    "ស្រុកស្វាយជ្រំ",
    "ខណ្ឌសែនសុខ",
    "ខណ្ឌចំការមន",
    "ឃុំគគីរ",
    "ឃុំស្វាយរំពារ",
    "ឃុំត្រពាំងក្រសាំង",
    "សង្កាត់ទន្លេបាសាក់",
]

villages = [
    "ភូមិថ្មី",
    "ភូមិកណ្ដាល",
    "ភូមិព្រែក",
    "ភូមិជ្រោយ",
    "ភូមិសាមគ្គី",
    "ភូមិត្រពាំង",
]

names = [
    "សុខ សុភ័ក្រ",
    "ចាន់ សុវណ្ណ",
    "ស្រី វណ្ណា",
    "លី សុភា",
    "ហេង ដារ៉ា",
    "ពៅ រតនា",
    "មុនី សំណាង",
    "សុជាតិ ពេជ្រ",
]

def khmer_digits(s):
    return str(s).translate(str.maketrans("0123456789", "០១២៣៤៥៦៧៨៩"))

def random_id():
    return khmer_digits("".join(random.choice("0123456789") for _ in range(9)))

def random_date(y1=1970, y2=2038):
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(y1, y2)
    return khmer_digits(f"{d:02d}.{m:02d}.{y}")

def random_address():
    return f"{random.choice(villages)} {random.choice(places)} {random.choice(places)} {random.choice(places)}"

def sample_text():
    group = random.choice(["short", "place", "address", "name", "number", "date"])
    if group == "short":
        return random.choice(short_fields)
    if group == "place":
        return random.choice(places)
    if group == "address":
        return random_address()
    if group == "name":
        return random.choice(names)
    if group == "number":
        return random_id()
    return random_date()

def add_noise(img):
    if random.random() < 0.35:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.1, 0.45)))

    if random.random() < 0.40:
        angle = random.uniform(-1.2, 1.2)
        img = img.rotate(angle, expand=True, fillcolor=(245, 245, 235))

    return img

def render_text_crop(text, filename):
    # Width changes by text length
    width = max(220, min(760, 80 + len(text) * 22))
    height = random.choice([48, 52, 56, 60])

    bg = random.choice([
        (250, 250, 240),
        (245, 248, 235),
        (240, 245, 230),
        (250, 245, 230),
        (235, 242, 225),
    ])

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    font_size = random.choice([22, 24, 26, 28, 30, 32])
    font = ImageFont.truetype(FONT_PATH, font_size)

    x = random.randint(8, 18)
    y = random.randint(6, 14)

    color = random.choice([(15, 15, 15), (35, 35, 35), (55, 55, 55)])
    draw.text((x, y), text, font=font, fill=color)

    # faint background lines
    if random.random() < 0.35:
        for line_y in range(0, height, random.randint(10, 16)):
            draw.line((0, line_y, width, line_y), fill=(225, 225, 215), width=1)

    img = add_noise(img)
    img.save(IMG_DIR / filename, quality=95)

def create_dataset(n=3000):
    rows = []

    for i in range(1, n + 1):
        text = sample_text()
        filename = f"focus_{i:06d}.jpg"
        render_text_crop(text, filename)
        rows.append(f"images/{filename}\t{text}")

    random.shuffle(rows)

    val_count = max(1, int(len(rows) * 0.1))
    val_rows = rows[:val_count]
    train_rows = rows[val_count:]

    with open(OUT_DIR / "train_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(train_rows))

    with open(OUT_DIR / "val_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(val_rows))

    print("Done generating focused Khmer ID OCR crops")
    print("Output folder:", OUT_DIR)
    print("Total images:", len(rows))
    print("Train:", len(train_rows))
    print("Val:", len(val_rows))
    print("Example:")
    print(rows[0])

if __name__ == "__main__":
    create_dataset(n=3000)