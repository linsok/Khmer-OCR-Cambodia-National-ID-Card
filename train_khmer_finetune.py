from types import SimpleNamespace
from kiri_ocr.training import train_command

args = SimpleNamespace(
    # Dataset
    train_labels="data/khmer_rec/train_label.txt",
    val_labels="data/khmer_rec/val_label.txt",

    # Output folder
    output_dir="output/khmer_finetune",

    # Pretrained Kiri OCR model
    from_model=r"C:\Users\User\.cache\huggingface\hub\models--mrrtmob--kiri-ocr\snapshots\3a3819874ad67a3a9624d5d994c46649060d7dc9\model.safetensors",

    # Training setup
    device="cuda",   # If no GPU, Kiri will use CPU automatically
    epochs=3,
    batch_size=4,
    lr=1e-5,
    weight_decay=0.01,
    resume=False,

    # Image size
    height=48,
    width=640,

    # Vocabulary
    vocab=None,

    # Loss weights
    ctc_weight=0.5,
    dec_weight=0.5,

    # Sequence length
    max_seq_len=128,

    # Hugging Face dataset options not used here
    hf_dataset=None,
    hf_subset=None,
    hf_train_split="train",
    hf_val_split=None,
    hf_val_percent=0.1,
    hf_image_col="image",
    hf_text_col="text",

    # Architecture settings
    encoder_dim=None,
    encoder_heads=None,
    encoder_layers=None,
    encoder_ffn_dim=None,
    decoder_dim=None,
    decoder_heads=None,
    decoder_layers=None,
    decoder_ffn_dim=None,
    dropout=None,
)

train_command(args)