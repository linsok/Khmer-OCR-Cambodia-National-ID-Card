from pathlib import Path
import random

DATA_DIR = Path("data/khmer_real_card_lines_v1")
ALL_LABEL = DATA_DIR / "all_label.txt"

random.seed(2026)

rows = []

if not ALL_LABEL.exists():
    raise FileNotFoundError(f"Missing label file: {ALL_LABEL}")

with open(ALL_LABEL, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        if "\t" not in line:
            print("Skipping bad line without TAB:", repr(line))
            continue

        img_rel, text = line.split("\t", 1)

        img_path = DATA_DIR / img_rel
        if not img_path.exists():
            print("Skipping missing image:", img_path)
            continue

        rows.append((img_rel, text))

if not rows:
    raise ValueError("No valid rows found in all_label.txt")

random.shuffle(rows)

val_count = max(1, int(len(rows) * 0.15))
val_rows = rows[:val_count]
train_rows = rows[val_count:]

with open(DATA_DIR / "train_label.txt", "w", encoding="utf-8") as f:
    for img_rel, text in train_rows:
        f.write(f"{img_rel}\t{text}\n")

with open(DATA_DIR / "val_label.txt", "w", encoding="utf-8") as f:
    for img_rel, text in val_rows:
        f.write(f"{img_rel}\t{text}\n")

print("Real card line dataset split complete.")
print("Train:", len(train_rows))
print("Val:", len(val_rows))
print("Total:", len(rows))

print("\nExample train row:")
print(f"{train_rows[0][0]}\t{train_rows[0][1]}")

print("\nExample val row:")
print(f"{val_rows[0][0]}\t{val_rows[0][1]}")