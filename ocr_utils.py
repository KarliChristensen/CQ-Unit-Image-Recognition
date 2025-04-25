# ocr_utils.py
import pytesseract
from PIL import Image
import os

def perform_ocr(image):
    """
    Performs OCR on the given image and returns the extracted text (cleaned).
    """
    try:
        text = pytesseract.image_to_string(image)
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
        # Simulate text on the image (replace with actual image loading)
        # For real testing, you'd do:
        # from PIL import ImageDraw, ImageFont
        # draw = ImageDraw.Draw(dummy_image)
        # font = ImageFont.load_default()
        # draw.text((10, 10), "Test Unit", fill='black', font=font)

        extracted_text = perform_ocr(dummy_image)
        if extracted_text is not None:
            print(f"Extracted text: '{extracted_text}'")
            output_folder = extracted_text
            os.makedirs(output_folder, exist_ok=True)
            print(f"Created dummy folder: '{output_folder}'")
        else:
            print("OCR failed.")
    except Exception as e:
        print(f"Error during direct test: {e}")