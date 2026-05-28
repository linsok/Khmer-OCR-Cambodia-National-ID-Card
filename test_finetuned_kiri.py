from pathlib import Path
from kiri_ocr import OCR

IMAGE_PATH = r"D:\kiri-ocr-test\khmer_line.jpg"

BASELINE_MODEL = "mrrtmob/kiri-ocr"

FINETUNED_MODEL = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v1\model.safetensors"

def run_ocr(model_name, model_path):
    print("\n" + "=" * 60)
    print(model_name)
    print("=" * 60)

    ocr = OCR(
        model_path=model_path,
        device="cpu",
        decode_method="accurate",
        verbose=True,
    )

    text, results = ocr.extract_text(IMAGE_PATH)

    print("\nOCR TEXT:")
    print(text)

    print("\nDETAILS:")
    for i, item in enumerate(results, start=1):
        print(f"Result {i}: {item}")

def main():
    if not Path(IMAGE_PATH).exists():
        print("Image not found:")
        print(IMAGE_PATH)
        return

    run_ocr("Original Kiri OCR baseline", BASELINE_MODEL)
    run_ocr("Fine-tuned Kiri OCR mixed ID v1", FINETUNED_MODEL)

if __name__ == "__main__":
    main()