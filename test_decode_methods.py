from pathlib import Path
from kiri_ocr import OCR

MODEL_PATHS = {
    "baseline": "mrrtmob/kiri-ocr",
    "v10_realid": r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v10_realid\model.safetensors",
    "v11_realid_fix": r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v11_realid_fix\model.safetensors",
}
DECODE_METHODS = ["accurate", "ctc", "decoder", "beam"]

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

def char_accuracy(pred, label):
    # Simple character-level similarity
    import difflib
    return difflib.SequenceMatcher(None, pred, label).ratio()

def run_one(ocr, img_path):
    text, results = ocr.extract_text(str(img_path))
    return text.strip().replace("\n", " ")

def main():
    samples = load_samples(100)

    for model_name, model_path in MODEL_PATHS.items():
        print("\n" + "=" * 70)
        print("MODEL:", model_name)
        print("=" * 70)

        for method in DECODE_METHODS:
            print("\nDecode method:", method)
            ocr = OCR(model_path=model_path, device="cpu", decode_method=method)

            exact = 0
            char_scores = []

            for img_path, label in samples:
                pred = run_one(ocr, img_path)
                exact += int(pred == label)
                char_scores.append(char_accuracy(pred, label))

            avg_char_acc = sum(char_scores) / len(char_scores)

            print(f"Exact correct: {exact}/{len(samples)}")
            print(f"Average character similarity: {avg_char_acc:.4f}")

if __name__ == "__main__":
    main()