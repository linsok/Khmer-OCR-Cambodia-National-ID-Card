from pathlib import Path
import cv2
import numpy as np


# Change this to your input card photo
INPUT_IMAGE = Path(r"D:\kiri-ocr-finetune\kiri-ocr\real_tests\my_id_card.jpg")

# Enhanced output
OUTPUT_IMAGE = INPUT_IMAGE.with_name(INPUT_IMAGE.stem + "_enhanced.jpg")


def resize_if_small(img, min_width=1200):
    h, w = img.shape[:2]
    if w >= min_width:
        return img

    scale = min_width / w
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)


def auto_contrast_bgr(img):
    # CLAHE on L channel improves local contrast without destroying color too much
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    l2 = clahe.apply(l)

    lab2 = cv2.merge((l2, a, b))
    return cv2.cvtColor(lab2, cv2.COLOR_LAB2BGR)


def denoise(img):
    # Good for phone-photo noise
    return cv2.fastNlMeansDenoisingColored(
        img,
        None,
        h=5,
        hColor=5,
        templateWindowSize=7,
        searchWindowSize=21
    )


def sharpen(img):
    # Unsharp mask
    blur = cv2.GaussianBlur(img, (0, 0), sigmaX=1.2)
    sharp = cv2.addWeighted(img, 1.7, blur, -0.7, 0)
    return sharp


def deskew_by_text_angle(img):
    """
    Mild deskew. This is safe for small rotation.
    If the card has strong perspective distortion, later we need card-corner detection.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold text-ish areas
    gray_blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(gray_blur, 50, 150)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=80,
        minLineLength=100,
        maxLineGap=10
    )

    if lines is None:
        return img

    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0:
            continue

        angle = np.degrees(np.arctan2(dy, dx))

        # only near-horizontal lines
        if -15 <= angle <= 15:
            angles.append(angle)

    if not angles:
        return img

    angle = float(np.median(angles))

    # avoid bad over-rotation
    if abs(angle) < 0.2 or abs(angle) > 8:
        return img

    h, w = img.shape[:2]
    center = (w // 2, h // 2)

    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img,
        matrix,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    print(f"Deskew angle: {angle:.2f}")
    return rotated


def enhance_for_ocr(input_path, output_path):
    img = cv2.imread(str(input_path))

    if img is None:
        raise FileNotFoundError(f"Could not read image: {input_path}")

    print("Original size:", img.shape[1], "x", img.shape[0])

    img = resize_if_small(img, min_width=1400)
    img = deskew_by_text_angle(img)
    img = denoise(img)
    img = auto_contrast_bgr(img)
    img = sharpen(img)

    # Save high quality
    cv2.imwrite(str(output_path), img, [int(cv2.IMWRITE_JPEG_QUALITY), 96])

    print("Enhanced saved:", output_path)
    print("Enhanced size:", img.shape[1], "x", img.shape[0])


if __name__ == "__main__":
    enhance_for_ocr(INPUT_IMAGE, OUTPUT_IMAGE)