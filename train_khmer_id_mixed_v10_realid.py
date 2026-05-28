from types import SimpleNamespace
from kiri_ocr.training import train_command

HF_MODEL_DIR = r"C:\Users\User\.cache\huggingface\hub\models--mrrtmob--kiri-ocr\snapshots\3a3819874ad67a3a9624d5d994c46649060d7dc9"

args = SimpleNamespace(
    # Dataset with real Khmer ID-card-style field labels
    train_labels="data/khmer_mixed_v8_realid/train_label.txt",
    val_labels="data/khmer_mixed_v8_realid/val_label.txt",

    # New output folder
    output_dir="output/khmer_id_mixed_v10_realid",

    # Original Kiri OCR vocab
    vocab=HF_MODEL_DIR + r"\vocab.json",

    # Continue from current best synthetic benchmark model
    from_model=r"D:\kiri-ocr-finetune\kiri-ocr\output\khmer_id_mixed_v9_errorfix3\model.safetensors",

    device="cuda",
    epochs=1,
    batch_size=4,

    # Small LR because the model is already good
    lr=1e-8,
    weight_decay=0.01,
    resume=False,

    height=48,
    width=640,

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