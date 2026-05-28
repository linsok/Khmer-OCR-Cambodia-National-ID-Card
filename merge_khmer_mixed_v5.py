from pathlib import Path
import shutil

BASE_DIR = Path("data/khmer_mixed_v4")
ERROR_FIX_DIR = Path("data/khmer_error_fix_v1")

OUT_DIR = Path("data/khmer_mixed_v5")
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
    base_train = read_labels(BASE_DIR / "train_label.txt")
    base_val = read_labels(BASE_DIR / "val_label.txt")

    err_train = read_labels(ERROR_FIX_DIR / "train_label.txt")
    err_val = read_labels(ERROR_FIX_DIR / "val_label.txt")

    train_rows = []
    val_rows = []

    copy_and_collect(base_train, BASE_DIR, train_rows)
    copy_and_collect(base_val, BASE_DIR, val_rows)

    copy_and_collect(err_train, ERROR_FIX_DIR, train_rows)
    copy_and_collect(err_val, ERROR_FIX_DIR, val_rows)

    save_labels(train_rows, OUT_DIR / "train_label.txt")
    save_labels(val_rows, OUT_DIR / "val_label.txt")

    print("Mixed v5 dataset created successfully.")
    print("Output folder:", OUT_DIR)
    print("Train samples:", len(train_rows))
    print("Val samples:", len(val_rows))
    print("Total images:", len(list(OUT_IMG_DIR.glob('*'))))

    if train_rows:
        print("Example train row:")
        print(f"{train_rows[0][0]}\t{train_rows[0][1]}")

if __name__ == "__main__":
    main()