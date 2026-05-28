from pathlib import Path
import shutil

# Source datasets
MIXED_V1_DIR = Path("data/khmer_mixed")
FOCUS_DIR = Path("data/khmer_id_focus")

# Output dataset
OUT_DIR = Path("data/khmer_mixed_v3")
OUT_IMG_DIR = OUT_DIR / "images"
OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)

def read_labels(label_path):
    rows = []
    with open(label_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t", 1)
            if len(parts) != 2:
                continue
            img_rel, text = parts
            rows.append((img_rel, text))
    return rows

def copy_and_collect(rows, src_base, collected):
    for img_rel, text in rows:
        src_img = src_base / img_rel
        dst_img = OUT_IMG_DIR / Path(img_rel).name

        if not src_img.exists():
            print(f"Missing image: {src_img}")
            continue

        shutil.copy2(src_img, dst_img)
        collected.append((f"images/{dst_img.name}", text))

def save_labels(rows, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for img_rel, text in rows:
            f.write(f"{img_rel}\t{text}\n")

def main():
    mixed_train = read_labels(MIXED_V1_DIR / "train_label.txt")
    mixed_val = read_labels(MIXED_V1_DIR / "val_label.txt")

    focus_train = read_labels(FOCUS_DIR / "train_label.txt")
    focus_val = read_labels(FOCUS_DIR / "val_label.txt")

    train_rows = []
    val_rows = []

    copy_and_collect(mixed_train, MIXED_V1_DIR, train_rows)
    copy_and_collect(mixed_val, MIXED_V1_DIR, val_rows)

    copy_and_collect(focus_train, FOCUS_DIR, train_rows)
    copy_and_collect(focus_val, FOCUS_DIR, val_rows)

    save_labels(train_rows, OUT_DIR / "train_label.txt")
    save_labels(val_rows, OUT_DIR / "val_label.txt")

    print("Mixed v3 dataset created successfully.")
    print("Output folder:", OUT_DIR)
    print("Train samples:", len(train_rows))
    print("Val samples:", len(val_rows))
    print("Total images:", len(list(OUT_IMG_DIR.glob('*'))))

    if train_rows:
        print("Example train row:")
        print(f"{train_rows[0][0]}\t{train_rows[0][1]}")

if __name__ == "__main__":
    main()