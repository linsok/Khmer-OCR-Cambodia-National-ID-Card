from pathlib import Path
from kiri_ocr import OCR
import difflib

MODEL_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v8_errorfix2\model.safetensors"

VAL_LABELS = Path("data/khmer_id_synth/val_label.txt")
DATA_DIR = Path("data/khmer_id_synth")

def load_samples(n=100):
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

def char_similarity(pred, label):
    return difflib.SequenceMatcher(None, pred, label).ratio()

def main():
    samples = load_samples(100)

    ocr = OCR(
        model_path=MODEL_PATH,
        device="cpu",
        decode_method="beam",
    )

    wrong = []
    correct = 0

    for img_path, label in samples:
        text, results = ocr.extract_text(str(img_path))
        pred = text.strip().replace("\n", " ")

        if pred == label:
            correct += 1
        else:
            wrong.append((img_path, label, pred, char_similarity(pred, label)))

    print("Correct:", correct, "/", len(samples))
    print("Wrong count:", len(wrong))
    print("=" * 70)

    for i, (img_path, label, pred, sim) in enumerate(wrong, start=1):
        print(f"\nWrong {i}")
        print("Image:", img_path)
        print("Label:", label)
        print("Pred: ", pred)
        print(f"Similarity: {sim:.4f}")

if __name__ == "__main__":
    main()