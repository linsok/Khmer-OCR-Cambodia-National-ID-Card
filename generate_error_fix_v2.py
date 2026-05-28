import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUT_DIR = Path("data/khmer_error_fix_v2")
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

random.seed(999)

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

# Exact difficult words from v7 error analysis
short_weak = [
    "ខ្មែរ",
    "ស្រី ច័ន្ទ",
    "កញ្ញា សំណាង",
    "ស្រុកបាទី កំពត",
    "ស្រុកបាទី ខេត្តតាកែវ",
    "ស្រុកកៀនស្វាយ សៀមរាប",
    "ខណ្ឌសែនសុខ សៀមរាប",
    "ស្រុកអង្គស្នួល កំពង់ចាម",
    "បាត់ដំបង",
    "កំពង់ចាម",
    "កំពង់ស្ពឺ",
    "កណ្ដាល",
    "កំពត",
    "ភ្នំពេញ",
    "សៀមរាប",
]

# Long lines from wrong examples, rewritten with cleaner realistic address endings.
long_addresses = [
    "ភូមិជ្រោយ សង្កាត់ទន្លេបាសាក់ ស្រុកស្វាយជ្រំ កំពត",
    "ភូមិកណ្ដាល ឃុំត្រពាំងក្រសាំង ស្រុកស្វាយជ្រំ បាត់ដំបង",
    "ភូមិជ្រោយ ឃុំគគីរ ស្រុកបាទី កណ្ដាល",
    "ភូមិជ្រោយ ឃុំស្វាយរំពារ ខណ្ឌសែនសុខ ភ្នំពេញ",
    "ភូមិសាមគ្គី ឃុំស្វាយរំពារ ស្រុកស្រីសន្ធរ កណ្ដាល",
    "ភូមិសាមគ្គី ឃុំព្រែកអញ្ចាញ ស្រុកស្រីសន្ធរ កំពត",
    "ភូមិសាមគ្គី សង្កាត់ទន្លេបាសាក់ ស្រុកអង្គស្នួល បាត់ដំបង",
    "ភូមិថ្មី ឃុំស្វាយរំពារ ស្រុកស្វាយជ្រំ សៀមរាប",
    "ភូមិកណ្ដាល សង្កាត់ទឹកថ្លា ខណ្ឌចំការមន កំពង់ចាម",
    "ភូមិកណ្ដាល សង្កាត់ទន្លេបាសាក់ ស្រុកស្វាយជ្រំ កណ្ដាល",
    "ភូមិជ្រោយ ឃុំព្រែកអញ្ចាញ ស្រុកអង្គស្នួល ស្វាយរៀង",
    "ភូមិព្រែក សង្កាត់ទន្លេបាសាក់ ស្រុកស្រីសន្ធរ ភ្នំពេញ",
    "ភូមិជ្រោយ សង្កាត់ទន្លេបាសាក់ ស្រុកស្រីសន្ធរ កំពង់ចាម",
]

# More valid Khmer-address-style variants to improve endings.
clean_address_templates = [
    "ភូមិជ្រោយ សង្កាត់ទន្លេបាសាក់ ខណ្ឌចំការមន រាជធានីភ្នំពេញ",
    "ភូមិកណ្ដាល សង្កាត់ទឹកថ្លា ខណ្ឌសែនសុខ រាជធានីភ្នំពេញ",
    "ភូមិព្រែក ឃុំគគីរ ស្រុកកៀនស្វាយ ខេត្តកណ្ដាល",
    "ភូមិជ្រោយ ឃុំគគីរ ស្រុកកៀនស្វាយ ខេត្តកណ្ដាល",
    "ភូមិសាមគ្គី ឃុំព្រែកអញ្ចាញ ស្រុកស្រីសន្ធរ ខេត្តកំពង់ចាម",
    "ភូមិត្រពាំង ឃុំត្រពាំងក្រសាំង ស្រុកបាទី ខេត្តតាកែវ",
    "ភូមិថ្មី ឃុំស្វាយរំពារ ស្រុកស្វាយជ្រំ ខេត្តស្វាយរៀង",
    "ភូមិជ្រោយ ឃុំស្វាយរំពារ ស្រុកស្វាយជ្រំ ខេត្តស្វាយរៀង",
    "ភូមិកណ្ដាល ឃុំត្រពាំងក្រសាំង ស្រុកបាទី ខេត្តតាកែវ",
    "ភូមិសាមគ្គី ឃុំព្រែកអញ្ចាញ ស្រុកមុខកំពូល ខេត្តកណ្ដាល",
]

def random_date():
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(1960, 2035)
    return khmer_digits(f"{d:02d}.{m:02d}.{y}")

def random_id():
    return khmer_digits("".join(random.choice("0123456789") for _ in range(9)))

def sample_text():
    r = random.random()

    # Highest weight: exact remaining wrong long lines
    if r < 0.40:
        return random.choice(long_addresses)

    # Clean realistic address variants
    if r < 0.65:
        return random.choice(clean_address_templates)

    # Short weak words
    if r < 0.82:
        return random.choice(short_weak)

    # Dates
    if r < 0.92:
        return random_date()

    # ID numbers, sometimes exact length only
    return random_id()

def add_noise(img):
    # Keep noise moderate because current errors are small character confusions
    if random.random() < 0.25:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.05, 0.25)))

    if random.random() < 0.25:
        angle = random.uniform(-0.6, 0.6)
        img = img.rotate(angle, expand=True, fillcolor=(245, 245, 235))

    if random.random() < 0.30:
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.90, 1.20))

    if random.random() < 0.30:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.92, 1.10))

    return img

def render_text_crop(text, filename):
    # Wide enough for long addresses so the model learns full endings
    width = max(300, min(1100, 120 + len(text) * 18))
    height = random.choice([52, 56, 60, 64])

    bg = random.choice([
        (245, 248, 238),
        (238, 246, 230),
        (250, 250, 240),
        (240, 245, 232),
    ])

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    font_size = random.choice([23, 24, 25, 26, 28])
    font = ImageFont.truetype(FONT_PATH, font_size)

    # faint ID-card-like lines
    if random.random() < 0.40:
        for y in range(0, height, random.randint(12, 18)):
            draw.line((0, y, width, y), fill=(224, 230, 218), width=1)

    x = random.randint(8, 16)
    y = random.randint(7, 14)

    draw.text(
        (x, y),
        text,
        font=font,
        fill=random.choice([(10, 10, 10), (30, 30, 30), (50, 50, 50)])
    )

    img = add_noise(img)
    img.save(IMG_DIR / filename, quality=random.choice([90, 95]))

def create_dataset(n=6000):
    rows = []

    for i in range(1, n + 1):
        text = sample_text()
        filename = f"errorfix_v2_{i:06d}.jpg"
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

    print("Done generating targeted error-fix v2 dataset")
    print("Output folder:", OUT_DIR)
    print("Total images:", len(rows))
    print("Train:", len(train_rows))
    print("Val:", len(val_rows))
    print("Example:")
    print(rows[0])

if __name__ == "__main__":
    create_dataset(n=6000)