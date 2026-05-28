import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUT_DIR = Path("data/khmer_error_fix_v1")
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

random.seed(888)

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

# Exact weak words from error analysis
weak_words = [
    "ខ្មែរ",
    "ស្រី",
    "ប្រុស",
    "កញ្ញា",
    "ច័ន្ទ",
    "ស្រុកបាទី",
    "ស្រុកអង្គស្នួល",
    "ស្រុកស្វាយជ្រំ",
    "ស្រុកស្រីសន្ធរ",
    "ខណ្ឌចំការមន",
    "ខណ្ឌសែនសុខ",
    "សង្កាត់ទន្លេបាសាក់",
    "សង្កាត់ទឹកថ្លា",
    "ឃុំព្រែកអញ្ចាញ",
    "ឃុំត្រពាំងក្រសាំង",
    "ភូមិជ្រោយ",
    "ភូមិសាមគ្គី",
    "ភូមិកណ្ដាល",
    "បាត់ដំបង",
    "កណ្ដាល",
    "កំពត",
    "កំពង់ចាម",
    "កំពង់ស្ពឺ",
    "ភ្នំពេញ",
    "ព្រៃវែង",
]

# Correct realistic address templates.
# Avoid unnatural random mixing too much.
address_templates = [
    "ភូមិជ្រោយ សង្កាត់ទន្លេបាសាក់ ខណ្ឌចំការមន រាជធានីភ្នំពេញ",
    "ភូមិកណ្ដាល សង្កាត់ទឹកថ្លា ខណ្ឌសែនសុខ រាជធានីភ្នំពេញ",
    "ភូមិជ្រោយ ឃុំគគីរ ស្រុកកៀនស្វាយ ខេត្តកណ្ដាល",
    "ភូមិសាមគ្គី ឃុំព្រែកអញ្ចាញ ស្រុកមុខកំពូល ខេត្តកណ្ដាល",
    "ភូមិត្រពាំង ឃុំត្រពាំងក្រសាំង ស្រុកបាទី ខេត្តតាកែវ",
    "ភូមិព្រែក ឃុំស្វាយរំពារ ស្រុកស្វាយជ្រំ ខេត្តស្វាយរៀង",
    "ភូមិសាមគ្គី ឃុំព្រែកអញ្ចាញ ស្រុកស្រីសន្ធរ ខេត្តកំពង់ចាម",
    "ភូមិជ្រោយ ឃុំស្វាយរំពារ ស្រុកស្វាយជ្រំ ខេត្តស្វាយរៀង",
    "ភូមិថ្មី ឃុំគគីរ ស្រុកបាទី ខេត្តតាកែវ",
    "ភូមិកណ្ដាល ឃុំត្រពាំងក្រសាំង ស្រុកបាទី ខេត្តតាកែវ",
]

name_templates = [
    "កញ្ញា សំណាង",
    "ស្រី ច័ន្ទ",
    "សុខ សុភ័ក្រ",
    "ចាន់ សុវណ្ណ",
    "ហេង ដារ៉ា",
    "លី សុភា",
    "មុនី សំណាង",
]

khmer_digits_map = str.maketrans("0123456789", "០១២៣៤៥៦៧៨៩")

def khmer_digits(s):
    return str(s).translate(khmer_digits_map)

def random_date():
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(1960, 2035)
    return khmer_digits(f"{d:02d}.{m:02d}.{y}")

def random_id():
    return khmer_digits("".join(random.choice("0123456789") for _ in range(9)))

def sample_text():
    r = random.random()

    # More long address samples because many errors are truncated addresses
    if r < 0.40:
        return random.choice(address_templates)

    # Weak isolated words and place names
    if r < 0.65:
        return random.choice(weak_words)

    # Name-like samples
    if r < 0.78:
        return random.choice(name_templates)

    # Dates because punctuation failed
    if r < 0.90:
        return random_date()

    # ID numbers
    return random_id()

def add_noise(img):
    if random.random() < 0.35:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.05, 0.35)))

    if random.random() < 0.30:
        angle = random.uniform(-0.8, 0.8)
        img = img.rotate(angle, expand=True, fillcolor=(245, 245, 235))

    if random.random() < 0.35:
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.85, 1.25))

    if random.random() < 0.35:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.90, 1.12))

    return img

def render_text_crop(text, filename):
    # Give long addresses enough width to avoid truncation during OCR/detection
    width = max(260, min(980, 100 + len(text) * 18))
    height = random.choice([48, 52, 56, 60, 64])

    bg = random.choice([
        (245, 248, 238),
        (238, 246, 230),
        (250, 250, 240),
        (240, 245, 232),
    ])

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    font_size = random.choice([22, 24, 26, 28, 30])
    font = ImageFont.truetype(FONT_PATH, font_size)

    # Faint document background lines
    if random.random() < 0.35:
        for y in range(0, height, random.randint(11, 17)):
            draw.line((0, y, width, y), fill=(225, 230, 218), width=1)

    x = random.randint(8, 16)
    y = random.randint(5, 12)

    draw.text((x, y), text, font=font, fill=random.choice([(10, 10, 10), (35, 35, 35), (55, 55, 55)]))

    img = add_noise(img)
    img.save(IMG_DIR / filename, quality=random.choice([90, 95]))

def create_dataset(n=5000):
    rows = []

    for i in range(1, n + 1):
        text = sample_text()
        filename = f"errorfix_{i:06d}.jpg"
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

    print("Done generating targeted error-fix dataset")
    print("Output folder:", OUT_DIR)
    print("Total images:", len(rows))
    print("Train:", len(train_rows))
    print("Val:", len(val_rows))
    print("Example:")
    print(rows[0])

if __name__ == "__main__":
    create_dataset(n=5000)