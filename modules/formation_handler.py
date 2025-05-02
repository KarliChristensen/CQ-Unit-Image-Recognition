# formation_handler.py

import pyautogui
from config import FORMATION_POTENTIAL_REGIONS, BOX_COLOR_TOLERANCE, BOX_GREY_RGB
from utils.functions import is_button_present, capture_hover_popup
from utils.navigation import move
from utils.ocr import perform_ocr_single_line

def capture_unit_formations():
    captured_formations = []
    for i, region in enumerate(FORMATION_POTENTIAL_REGIONS):
        if is_button_present(region, BOX_GREY_RGB, BOX_COLOR_TOLERANCE):
            filename = f"formation_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            captured_formations.append(filename)

            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            move((center_x, center_y))

            button_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_hover_popup(button_region, output_path=f"formations_popup_{i+1}.png")
        else:
            break
    return captured_formations

def ocr_formation_popup(button_region):
    try:
        button_left, button_top, button_width, button_height = button_region
        popup_left = button_left - 411 - 5
        popup_top = button_top - 25 - 5
        popup_width = 430
        line_height = 24
        title_padding = 30
        padding_top = 16
        padding_bottom = 22

        estimated_text_height = (button_top - 25) - (popup_top + title_padding)

        if estimated_text_height > 0 and popup_width > 0:
            screenshot = pyautogui.screenshot(region=(popup_left, popup_top, popup_width, (button_top - popup_top)))
            popup_image = screenshot.convert('RGB')
            popup_height = popup_image.height

            first_line_y_start = padding_top + title_padding
            full_text = []
            line_number = (popup_height - title_padding - padding_top - padding_bottom) // line_height if (popup_height - title_padding - padding_top - padding_bottom) > 0 else 0
            line_number = max(0, line_number)

            for i in range(line_number):
                line_y_start = first_line_y_start + i * line_height
                line_y_end = line_y_start + line_height
                line_region = (0, int(line_y_start), popup_width, int(line_y_end + 2)) # Add a couple of pixels
                cropped_line = popup_image.crop(line_region)
                line_text = perform_ocr_single_line(cropped_line, debug=True, threshold=True)
                if line_text:
                    full_text.append(line_text.strip())

            return " ".join(full_text).strip()
        else:
            print("Calculated popup dimensions are invalid for OCR.")
            return None

    except Exception as e:
        print(f"Error during formation popup OCR: {e}")
        return None