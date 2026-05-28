from pathlib import Path
import shutil

# -----------------------------
# Source datasets
# -----------------------------
REAL_DIR = Path("data/khmer_rec")
SYNTH_DIR = Path("data/khmer_id_synth")

# -----------------------------
# Output merged dataset
# -----------------------------
OUT_DIR = Path("data/khmer_mixed")
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

        # copy image into merged images folder
        shutil.copy2(src_img, dst_img)

        # store new label path using images/filename.jpg
        new_rel = f"images/{dst_img.name}"
        collected.append((new_rel, text))

def save_labels(rows, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for img_rel, text in rows:
            f.write(f"{img_rel}\t{text}\n")

def main():
    real_train = read_labels(REAL_DIR / "train_label.txt")
    real_val   = read_labels(REAL_DIR / "val_label.txt")

    synth_train = read_labels(SYNTH_DIR / "train_label.txt")
    synth_val   = read_labels(SYNTH_DIR / "val_label.txt")

    merged_train = []
    merged_val = []

    copy_and_collect(real_train, REAL_DIR, merged_train)
    copy_and_collect(real_val, REAL_DIR, merged_val)

    copy_and_collect(synth_train, SYNTH_DIR, merged_train)
    copy_and_collect(synth_val, SYNTH_DIR, merged_val)

    save_labels(merged_train, OUT_DIR / "train_label.txt")
    save_labels(merged_val, OUT_DIR / "val_label.txt")

    print("Merged dataset created successfully.")
    print("Output folder:", OUT_DIR)
    print("Train samples:", len(merged_train))
    print("Val samples:", len(merged_val))
    print("Total images:", len(list(OUT_IMG_DIR.glob('*'))))

    if merged_train:
        print("Example train row:")
        print(f"{merged_train[0][0]}\t{merged_train[0][1]}")

if __name__ == "__main__":
    main()