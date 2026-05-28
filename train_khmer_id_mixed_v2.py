from types import SimpleNamespace
from kiri_ocr.training import train_command

HF_MODEL_DIR = r"C:\Users\User\.cache\huggingface\hub\models--mrrtmob--kiri-ocr\snapshots\3a3819874ad67a3a9624d5d994c46649060d7dc9"

args = SimpleNamespace(
    # Mixed dataset: KhmerST + synthetic Khmer ID-style crops
    train_labels="data/khmer_mixed/train_label.txt",
    val_labels="data/khmer_mixed/val_label.txt",

    # New output folder
    output_dir="output/khmer_id_mixed_v2",

    # Original pretrained Kiri OCR files
    vocab=HF_MODEL_DIR + r"\vocab.json",
    from_model=HF_MODEL_DIR + r"\model.safetensors",

    # Training setup
    device="cuda",      # If no GPU, it will use CPU
    epochs=1,
    batch_size=4,

    # Small learning rate for safe fine-tuning
    lr=2e-7,
    weight_decay=0.01,
    resume=False,

    # Image size
    height=48,
    width=640,

    # Important change:
    # Give more weight to CTC because CTC decoding performed best
    ctc_weight=0.7,
    dec_weight=0.3,

    # Sequence length
    max_seq_len=260,

    # HF dataset options not used
    hf_dataset=None,
    hf_subset=None,
    hf_train_split="train",
    hf_val_split=None,
    hf_val_percent=0.1,
    hf_image_col="image",
    hf_text_col="text",

    # Correct architecture inferred from original Kiri OCR baseline
    encoder_dim=384,
    encoder_heads=6,
    encoder_layers=6,
    encoder_ffn_dim=1536,

    decoder_dim=384,
    decoder_heads=6,
    decoder_layers=4,
    decoder_ffn_dim=1536,

    dropout=0.15,
)

train_command(args)