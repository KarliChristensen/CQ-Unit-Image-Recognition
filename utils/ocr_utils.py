# ocr_utils.py

import pytesseract
from PIL import Image
import os
import cv2
import numpy as np

def perform_ocr(image, threshold=False, threshold_value=150):

    """
    Performs OCR on the given image and returns the extracted text (cleaned).
    Optionally applies thresholding before OCR.

    Args:
        image (PIL.Image.Image): The image to perform OCR on.
        threshold (bool, optional): Whether to apply thresholding. Defaults to False.
        threshold_value (int, optional): The threshold value to use if threshold is True. Defaults to 150.
    """
    
    try:
        img = image.convert('L')

        if threshold:
            img_np = np.array(img)
            _, thresh_img_np = cv2.threshold(img_np, threshold_value, 255, cv2.THRESH_BINARY)
            img = Image.fromarray(thresh_img_np)

        text = pytesseract.image_to_string(img)
        cleaned_text = text.strip()
        cleaned_text = ''.join(char for char in cleaned_text if char.isalnum() or char.isspace())
        cleaned_text = cleaned_text.replace(" ", "_")
        return cleaned_text
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred during OCR: {e}")
        return None

if __name__ == "__main__":
    # Example usage if you run this file directly
    try:
        # Create a dummy image for testing
        dummy_image = Image.new('RGB', (100, 30), color='white')
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(dummy_image)
        font = ImageFont.load_default()
        draw.text((10, 10), "Test Unit 123", fill='black', font=font)

        # Test without thresholding
        extracted_text_no_thresh = perform_ocr(dummy_image)
        if extracted_text_no_thresh is not None:
            print(f"Extracted text (no threshold): '{extracted_text_no_thresh}'")
        else:
            print("OCR failed (no threshold).")

        # Test with thresholding
        extracted_text_thresh = perform_ocr(dummy_image, threshold=True, threshold_value=100)
        if extracted_text_thresh is not None:
            print(f"Extracted text (with threshold): '{extracted_text_thresh}'")
        else:
            print("OCR failed (with threshold).")

        output_folder = "test_output"
        os.makedirs(output_folder, exist_ok=True)
        print(f"Created dummy folder: '{output_folder}'")

    except Exception as e:
        print(f"Error during direct test: {e}")