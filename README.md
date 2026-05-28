# Khmer OCR for Cambodia National ID Card

This project focuses on fine-tuning and building an OCR pipeline for Khmer text recognition on Cambodia National ID card fields.

## Project Overview

The system is designed to extract structured information from Cambodia National ID card images, including:

- Khmer name
- Latin name
- ID number
- Date of birth
- Gender
- Height
- Birth place
- Address
- Validity dates
- Body mark
- MRZ lines

## Main Pipeline

The current OCR pipeline includes:

1. Khmer OCR model fine-tuning based on Kiri OCR
2. Synthetic Khmer ID-style dataset generation
3. Error-fix dataset generation
4. Real-ID-style dataset generation
5. Full-card text line detection
6. Dynamic MRZ line detection
7. Field mapping and post-processing
8. JSON output extraction

## Best Fine-Tuned Model Result

Best tested model:

```text
v11_realid_fix + beam decoding
Exact match accuracy: 82%
Average character similarity: 97.59%
Validation CTC accuracy: 58.87%


# Kiri OCR 📄

[![PyPI version](https://badge.fury.io/py/kiri-ocr.svg)](https://badge.fury.io/py/kiri-ocr)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Versions](https://img.shields.io/pypi/pyversions/kiri-ocr.svg)](https://pypi.org/project/kiri-ocr/)
[![Downloads](https://static.pepy.tech/badge/kiri-ocr)](https://pepy.tech/project/kiri-ocr)
[![Hugging Face Model](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Model-yellow)](https://huggingface.co/mrrtmob/kiri-ocr)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/mrrtmob/kiri-ocr)

**Kiri OCR** is a lightweight OCR library for **English and Khmer** documents. It provides document-level text detection, recognition, and rendering capabilities.

[**🚀 Try the Live Demo**](https://huggingface.co/spaces/mrrtmob/kiri-ocr) | [**📚 Full Documentation**](https://github.com/mrrtmob/kiri-ocr/wiki)

![Kiri OCR](https://raw.githubusercontent.com/mrrtmob/kiri-ocr/main/assets/image.png)

## ✨ Key Features

- **High Accuracy**: Transformer model with hybrid CTC + attention decoder
- **Bi-lingual**: Native support for English and Khmer (and mixed text)
- **Document Processing**: Automatic text line and word detection
- **Streaming**: Real-time character-by-character output (like LLM streaming)
- **Easy to Use**: Simple Python API and CLI

## 📦 Installation

```bash
pip install kiri-ocr
```

## 💻 Quick Start

### CLI Tool

```bash
kiri-ocr document.jpg
```

### Python API

```python
from kiri_ocr import OCR

# Initialize (auto-downloads from Hugging Face)
ocr = OCR()

# Extract text from document
text, results = ocr.extract_text('document.jpg')
print(text)

# Get detailed box-by-box results
for line in results:
    print(f"{line['text']} (confidence: {line['confidence']:.1%})")
```

### Decoding Methods

Choose the decoding method based on your speed/quality tradeoff:

```python
# Fast (CTC) - Fastest, good for batch processing
ocr = OCR(decode_method="fast")

# Accurate (Decoder) - Balanced speed and quality (default)
ocr = OCR(decode_method="accurate")

# Beam Search - Best quality, slowest
ocr = OCR(decode_method="beam")
```

### Streaming Recognition

Get character-by-character output like LLM streaming:

```python
from kiri_ocr import OCR

ocr = OCR(decode_method="accurate")

# Stream characters as they're decoded
for chunk in ocr.extract_text_stream_chars('document.jpg'):
    print(chunk['token'], end='', flush=True)
    if chunk['document_finished']:
        print()  # Done!
```

## 📚 Documentation

Full documentation is available on the [**Wiki**](https://github.com/mrrtmob/kiri-ocr/wiki):

- [Installation](https://github.com/mrrtmob/kiri-ocr/wiki/Installation)
- [Quick Start Guide](https://github.com/mrrtmob/kiri-ocr/wiki/Quick-Start)
- [Python API Reference](https://github.com/mrrtmob/kiri-ocr/wiki/Python-API)
- [CLI Reference](https://github.com/mrrtmob/kiri-ocr/wiki/CLI-Reference)
- [Training Guide](https://github.com/mrrtmob/kiri-ocr/wiki/Training-Guide)
- [Detector API](https://github.com/mrrtmob/kiri-ocr/wiki/Detector-API)
- [Architecture](https://github.com/mrrtmob/kiri-ocr/wiki/Architecture)

## 📊 Benchmark

Results on synthetic test images (10 popular fonts):

![Benchmark Graph](https://raw.githubusercontent.com/mrrtmob/kiri-ocr/main/benchmark/benchmark_graph.png)

## 📁 Project Structure

```
kiri_ocr/
├── core.py               # OCR class
├── model.py              # Transformer model
├── training.py           # Training code
├── cli.py                # Command-line interface
└── detector/             # Text detection
    ├── db/               # DB detector
    └── craft/            # CRAFT detector
```

## ☕ Support

If you find this project useful:

- ⭐ Star this repository
- [Buy Me a Coffee](https://buymeacoffee.com/tmob)
- [ABA Payway](https://link.payway.com.kh/ABAPAYfd4073965)

[**Join our Discord Community**]([https://discord.gg/jnNbhSaYQ9)](https://discord.gg/Vcrw274RVC)

## ⚖️ License

[Apache License 2.0](https://github.com/mrrtmob/kiri-ocr/blob/main/LICENSE)

