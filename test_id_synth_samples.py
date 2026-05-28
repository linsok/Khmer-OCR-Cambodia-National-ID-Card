from pathlib import Path
from kiri_ocr import OCR

BASELINE_MODEL = "mrrtmob/kiri-ocr"
MIXED_MODEL = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v1\model.safetensors"

VAL_LABELS = Path("data/khmer_id_synth/val_label.txt")
DATA_DIR = Path("data/khmer_id_synth")

def load_samples(n=10):
    rows = []
    with open(VAL_LABELS, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            img_rel, label = line.split("\t", 1)
            rows.append((DATA_DIR / img_rel, label))
            if len(rows) >= n:
                break
    return rows

def run_one(ocr, img_path):
    text, results = ocr.extract_text(str(img_path))
    return text.strip().replace("\n", " ")

def main():
    samples = load_samples(10)

    print("Loading baseline...")
    baseline = OCR(model_path=BASELINE_MODEL, device="cpu", decode_method="accurate")

    print("Loading mixed fine-tuned model...")
    mixed = OCR(model_path=MIXED_MODEL, device="cpu", decode_method="accurate")

    baseline_correct = 0
    mixed_correct = 0

    for i, (img_path, label) in enumerate(samples, start=1):
        b_pred = run_one(baseline, img_path)
        m_pred = run_one(mixed, img_path)

        b_ok = b_pred == label
        m_ok = m_pred == label

        baseline_correct += int(b_ok)
        mixed_correct += int(m_ok)

        print("\n" + "=" * 60)
        print(f"Sample {i}")
        print("Image:", img_path)
        print("Label:   ", label)
        print("Baseline:", b_pred, "OK" if b_ok else "WRONG")
        print("Mixed:   ", m_pred, "OK" if m_ok else "WRONG")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"Baseline exact correct: {baseline_correct}/{len(samples)}")
    print(f"Mixed exact correct:    {mixed_correct}/{len(samples)}")

if __name__ == "__main__":
    main()