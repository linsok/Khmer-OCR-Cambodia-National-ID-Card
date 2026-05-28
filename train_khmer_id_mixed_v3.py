from types import SimpleNamespace
from kiri_ocr.training import train_command

HF_MODEL_DIR = r"C:\Users\User\.cache\huggingface\hub\models--mrrtmob--kiri-ocr\snapshots\3a3819874ad67a3a9624d5d994c46649060d7dc9"

args = SimpleNamespace(
    # Mixed v3 dataset: KhmerST + ID-style + focused weak cases
    train_labels="data/khmer_mixed_v3/train_label.txt",
    val_labels="data/khmer_mixed_v3/val_label.txt",

    output_dir="output/khmer_id_mixed_v3",

    vocab=HF_MODEL_DIR + r"\vocab.json",
    from_model=HF_MODEL_DIR + r"\model.safetensors",

    device="cuda",   # uses CPU if no GPU
    epochs=1,
    batch_size=4,

    # Best stable setting from mixed v1
    lr=2e-7,
    weight_decay=0.01,
    resume=False,

    height=48,
    width=640,

    # Best loss balance so far
    ctc_weight=0.5,
    dec_weight=0.5,

    max_seq_len=260,

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