from types import SimpleNamespace
from kiri_ocr.training import train_command

HF_MODEL_DIR = r"C:\Users\User\.cache\huggingface\hub\models--mrrtmob--kiri-ocr\snapshots\3a3819874ad67a3a9624d5d994c46649060d7dc9"

args = SimpleNamespace(
    # Dataset
    train_labels="data/khmer_rec/train_label.txt",
    val_labels="data/khmer_rec/val_label.txt",

    # Output folder
    output_dir="output/khmer_finetune_v3",

    # Original pretrained Kiri OCR files
    vocab=HF_MODEL_DIR + r"\vocab.json",
    from_model=HF_MODEL_DIR + r"\model.safetensors",

    # Training setup
    device="cuda",      # If no GPU, it will use CPU
    epochs=1,           # Test only 1 epoch first
    batch_size=4,
    lr=1e-6,
    weight_decay=0.01,
    resume=False,

    # Image size
    height=48,
    width=640,

    # Loss weights
    ctc_weight=0.5,
    dec_weight=0.5,

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

    # Correct architecture based on checkpoint tensor shapes
    encoder_dim=384,
    encoder_heads=8,
    encoder_layers=4,
    encoder_ffn_dim=1536,

    decoder_dim=384,
    decoder_heads=8,
    decoder_layers=3,
    decoder_ffn_dim=1536,

    dropout=0.15,
)

train_command(args)