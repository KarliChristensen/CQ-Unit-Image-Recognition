import pytesseract
from PIL import Image
import cv2
import numpy as np

def perform_ocr(image, threshold=False, threshold_value=150, psm=None):

    try:
        img = image.convert('L')

        if threshold:
            img_np = np.array(img)
            _, thresh_img_np = cv2.threshold(img_np, threshold_value, 255, cv2.THRESH_BINARY)
            img = Image.fromarray(thresh_img_np)

        config = ''
        if psm:
            config += f'--psm {psm}'

        text = pytesseract.image_to_string(img, config=config)
        cleaned_text = text.strip()
        # Keep digits, decimal points, and hyphens
        cleaned_text = ''.join(char for char in cleaned_text if char.isalnum() or char in ['.', '-'])
        return cleaned_text
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred during OCR: {e}")
        return None