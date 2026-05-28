from pathlib import Path

DATA_DIR = Path("data/khmer_real_card_lines_v1")
LABEL = DATA_DIR / "all_label.txt"
IMG_DIR = DATA_DIR / "images"

missing = []
existing = []
bad = []

with open(LABEL, "r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, start=1):
        raw = line.rstrip("\n")

        if not raw.strip():
            continue

        if "\t" not in raw:
            bad.append((line_no, raw, "no tab"))
            continue

        img_rel, text = raw.split("\t", 1)
        img_rel = img_rel.strip()
        img_path = DATA_DIR / img_rel

        if img_path.exists():
            existing.append((line_no, img_rel, text))
        else:
            missing.append((line_no, img_rel, text))

print("Total rows with existing images:", len(existing))
print("Missing rows:", len(missing))
print("Bad rows:", len(bad))
print("Images in folder:", len(list(IMG_DIR.glob('*'))))

print("\nMissing examples:")
for line_no, img_rel, text in missing[:50]:
    print(f"Line {line_no}: {img_rel}")

print("\nBad examples:")
for line_no, raw, reason in bad[:20]:
    print(f"Line {line_no}: {reason}: {repr(raw)}")