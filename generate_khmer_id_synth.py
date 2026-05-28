import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = Path("data/khmer_id_synth")
IMG_DIR = OUT_DIR / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

# Try Khmer-capable fonts on Windows
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
    raise FileNotFoundError("No Khmer font found. Please install Khmer UI or Noto Sans Khmer.")

FONT_PATH = find_font()
print("Using font:", FONT_PATH)

khmer_first_names = [
    "សុខ", "ចាន់", "ស្រី", "វណ្ណ", "ពៅ", "លី", "ហេង", "សុភា", "ដារ៉ា", "វិសាល",
    "កញ្ញា", "រតនា", "សុវណ្ណ", "មុនី", "សុជាតិ", "នារី", "បូរ៉ា", "សំបូរ"
]

khmer_last_names = [
    "សុភ័ក្រ", "សុវណ្ណ", "វណ្ណា", "សីហា", "ច័ន្ទ", "ពិសី", "រដ្ឋា", "មករា",
    "សុធា", "ធីតា", "វាសនា", "សុភី", "កុសល", "សំណាង", "ពេជ្រ"
]

provinces = [
    "ភ្នំពេញ", "កណ្ដាល", "កំពង់ចាម", "តាកែវ", "បាត់ដំបង", "សៀមរាប",
    "កំពត", "ព្រៃវែង", "ស្វាយរៀង", "កំពង់ស្ពឺ"
]

districts = [
    "ខណ្ឌចំការមន", "ខណ្ឌសែនសុខ", "ស្រុកកៀនស្វាយ", "ស្រុកបាទី",
    "ស្រុកស្រីសន្ធរ", "ស្រុកអង្គស្នួល", "ស្រុកស្វាយជ្រំ"
]

communes = [
    "សង្កាត់ទន្លេបាសាក់", "សង្កាត់ទឹកថ្លា", "ឃុំគគីរ", "ឃុំត្រពាំងក្រសាំង",
    "ឃុំព្រែកអញ្ចាញ", "ឃុំស្វាយរំពារ"
]

villages = [
    "ភូមិថ្មី", "ភូមិកណ្ដាល", "ភូមិព្រែក", "ភូមិជ្រោយ", "ភូមិសាមគ្គី",
    "ភូមិត្រពាំង"
]

field_labels = [
    "គោត្តនាម និងនាម",
    "លេខអត្តសញ្ញាណបណ្ណ",
    "ភេទ",
    "ថ្ងៃខែឆ្នាំកំណើត",
    "ទីកន្លែងកំណើត",
    "អាសយដ្ឋាន",
    "សញ្ជាតិ",
    "សុពលភាព"
]

def khmer_digits(num_str):
    table = str.maketrans("0123456789", "០១២៣៤៥៦៧៨៩")
    return str(num_str).translate(table)

def random_name():
    return random.choice(khmer_first_names) + " " + random.choice(khmer_last_names)

def random_id_number():
    return khmer_digits("".join(random.choice("0123456789") for _ in range(9)))

def random_date(start_year=1970, end_year=2005):
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(start_year, end_year)
    return khmer_digits(f"{d:02d}.{m:02d}.{y}")

def random_address():
    return (
        random.choice(villages) + " " +
        random.choice(communes) + " " +
        random.choice(districts) + " " +
        random.choice(provinces)
    )

def make_fake_record():
    gender = random.choice(["ប្រុស", "ស្រី"])
    birth_place = random.choice(districts) + " " + random.choice(provinces)
    return {
        "name": random_name(),
        "id_number": random_id_number(),
        "gender": gender,
        "dob": random_date(1970, 2005),
        "birth_place": birth_place,
        "address": random_address(),
        "nationality": "ខ្មែរ",
        "valid_until": random_date(2028, 2038),
    }

def add_noise(img):
    # Small blur/noise/rotation to imitate scanned or phone-captured crops
    if random.random() < 0.25:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 0.6)))

    if random.random() < 0.35:
        angle = random.uniform(-1.5, 1.5)
        img = img.rotate(angle, expand=True, fillcolor=(245, 245, 235))

    return img

def render_text_crop(text, filename, width=520, height=56):
    bg = random.choice([
        (250, 250, 240),
        (245, 248, 235),
        (240, 245, 230),
        (250, 245, 230),
    ])

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    font_size = random.choice([24, 26, 28, 30])
    font = ImageFont.truetype(FONT_PATH, font_size)

    x = random.randint(8, 18)
    y = random.randint(8, 14)

    # Slight grey/black text like document print
    color = random.choice([(20, 20, 20), (40, 40, 40), (55, 55, 55)])
    draw.text((x, y), text, font=font, fill=color)

    # Add faint horizontal line/background pattern sometimes
    if random.random() < 0.25:
        for line_y in range(0, height, random.randint(12, 18)):
            draw.line((0, line_y, width, line_y), fill=(225, 225, 215), width=1)

    img = add_noise(img)
    img.save(IMG_DIR / filename, quality=95)

def create_dataset(num_records=500):
    rows = []
    idx = 0

    for _ in range(num_records):
        rec = make_fake_record()

        samples = [
            rec["name"],
            rec["id_number"],
            rec["gender"],
            rec["dob"],
            rec["birth_place"],
            rec["address"],
            rec["nationality"],
            rec["valid_until"],
        ]

        for text in samples:
            idx += 1
            filename = f"id_field_{idx:06d}.jpg"
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

    print("Done generating synthetic Khmer ID-style OCR crops")
    print("Output folder:", OUT_DIR)
    print("Total images:", len(rows))
    print("Train:", len(train_rows))
    print("Val:", len(val_rows))
    print("Example label:")
    print(rows[0])

if __name__ == "__main__":
    create_dataset(num_records=500)