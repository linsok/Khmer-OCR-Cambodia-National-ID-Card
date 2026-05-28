from kiri_ocr import OCR

MODEL_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v10_realid\model.safetensors"
IMAGE_PATH = r"D:\kiri-ocr-finetune\kiri-ocr\real_tests\my_id_card.jpg"

ocr = OCR(
    model_path=MODEL_PATH,
    device="cpu",
    decode_method="beam",
)

text, results = ocr.extract_text(IMAGE_PATH)

print("\nOCR TEXT:")
print(text)

print("\nDETAILS:")
for r in results:
    print(r)