from pathlib import Path
from kiri_ocr import OCR

# Change this image path to any Khmer ID-card field crop or document image
IMAGE_PATH = r"D:\kiri-ocr-test\id_fields_v3\physical_marks.jpg"

BEST_MODEL = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v3\model.safetensors"

def main():
    image_path = Path(IMAGE_PATH)

    if not image_path.exists():
        print("Image not found:")
        print(image_path)
        return

    print("Loading best fine-tuned Khmer ID OCR model...")
    ocr = OCR(
        model_path=BEST_MODEL,
        device="cpu",
        decode_method="ctc",
        verbose=True,
    )

    print("Running OCR on:")
    print(image_path)

    text, results = ocr.extract_text(str(image_path))

    print("\n================ OCR TEXT ================\n")
    print(text)

    print("\n================ DETAILS ================\n")
    for i, item in enumerate(results, start=1):
        print(f"Line {i}")
        print("Text:", item.get("text"))
        print("Recognition confidence:", item.get("confidence"))
        print("Detection confidence:", item.get("det_confidence"))
        print("Box:", item.get("box"))
        print("--------------------------------")

if __name__ == "__main__":
    main()