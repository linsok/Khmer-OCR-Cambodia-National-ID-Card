from pathlib import Path
import shutil

OUT_DIR = Path("data/khmer_mixed_v7")
OUT_IMG = OUT_DIR / "images"

SRC_DATASETS = [
    Path("data/khmer_mixed_v6"),
    Path("data/khmer_error_fix_v3"),
]

# Oversample targeted dataset
OVERSAMPLE = {
    "khmer_mixed_v6": 1,
    "khmer_error_fix_v3": 2,   # important hard-case dataset
}

def read_labels(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(line)
    return rows

def copy_images(src_img_dir, dst_img_dir):
    dst_img_dir.mkdir(parents=True, exist_ok=True)
    for img in src_img_dir.iterdir():
        if img.is_file():
            dst = dst_img_dir / img.name
            if not dst.exists():
                shutil.copy2(img, dst)

def main():
    OUT_IMG.mkdir(parents=True, exist_ok=True)

    train_rows = []
    val_rows = []

    for ds in SRC_DATASETS:
        name = ds.name
        repeat = OVERSAMPLE.get(name, 1)

        print(f"Processing {name} (x{repeat})")

        copy_images(ds / "images", OUT_IMG)

        train_part = read_labels(ds / "train_label.txt")
        val_part = read_labels(ds / "val_label.txt")

        for _ in range(repeat):
            train_rows.extend(train_part)
            val_rows.extend(val_part)

    with open(OUT_DIR / "train_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(train_rows))

    with open(OUT_DIR / "val_label.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(val_rows))

    print("Mixed v7 dataset created successfully.")
    print("Output folder:", OUT_DIR)
    print("Train samples:", len(train_rows))
    print("Val samples:", len(val_rows))
    print("Total images:", len(list(OUT_IMG.iterdir())))

    if train_rows:
        print("Example train row:")
        print(train_rows[0].replace("\t", "  "))

if __name__ == "__main__":
    main()