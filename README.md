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
