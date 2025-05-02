# trait_handler.py

import autoit, pyautogui, time
from PIL import Image
import cv2
import numpy as np
from utils.ocr import perform_ocr_type, perform_ocr_single_line, perform_ocr
from utils.functions import colors_are_similar, hex_to_rgb, save_element
from utils.navigation import move
from config import UNIT_TRAIT_COLOR_TOLERANCE, UNIT_TRAIT_POTENTIAL_REGIONS, UNIT_TRAIT_TARGET_COLORS_RGB

def get_trait_color(region, target_colors_rgb, tolerance):
    x, y, w, h = region
    bracket_offset_x = 1
    bracket_offset_y = 14

    sample_x = x + bracket_offset_x
    sample_y = y + bracket_offset_y

    pixel_color = autoit.pixel_get_color(sample_x, sample_y)
    r = (pixel_color >> 16) & 0xFF
    g = (pixel_color >> 8) & 0xFF
    b = pixel_color & 0xFF
    current_rgb = (r, g, b)

    for target_rgb in target_colors_rgb:
        if all(abs(current - target) < tolerance for current, target in zip(current_rgb, target_rgb)):
            if target_rgb == (UNIT_TRAIT_TARGET_COLORS_RGB[0]):
                return "green"
            elif target_rgb == (UNIT_TRAIT_TARGET_COLORS_RGB[1]):
                return "red"
            elif target_rgb == (UNIT_TRAIT_TARGET_COLORS_RGB[2]):
                return "gray"
            else:
                return "unknown"
    return None

def is_trait_present(region, target_colors_rgb, tolerance):
    x, y, w, h = region
    bracket_offset_x = 1
    bracket_offset_y = 14

    sample_x = x + bracket_offset_x
    sample_y = y + bracket_offset_y

    try:
        pixel_color = autoit.pixel_get_color(sample_x, sample_y)
        r = (pixel_color >> 16) & 0xFF
        g = (pixel_color >> 8) & 0xFF
        b = pixel_color & 0xFF
        current_rgb = (r, g, b)
    except Exception as e:
        return False

    for target_color in target_colors_rgb:
        if all(abs(current - target) < tolerance for current, target in zip(current_rgb, target_color)):
            return True
    return False

def get_trait_popup_boundaries(button_region):
    button_left, button_top, button_width, button_height = button_region
    screen_width, screen_height = pyautogui.size()
    white_colors_hex = ["#8C8C8C", "#6B6B6C", "#CDCDCD", "#454546"]
    white_colors_rgb = [hex_to_rgb(hex_code) for hex_code in white_colors_hex]
    bottom_line_offset_fixed = 58
    text_block_x_offset_fixed = 1795 + 57
    line_spacing_fixed = 30
    popup_left_fixed = 1785 + 47
    popup_right_fixed = 2143 + 47
    popup_bottom_est = button_top - 36
    search_distance_lines_fixed = 10
    horizontal_check_offset_fixed = 5
    top_padding_fixed = 25

    center_x = button_left + button_width // 2
    center_y = button_top + button_height // 2
    move((center_x, center_y))
    time.sleep(0.05)

    start_search_y = max(0, int(popup_bottom_est - bottom_line_offset_fixed))
    start_x_center_approx = int(text_block_x_offset_fixed + 10)

    popup_top = find_white_text_top(start_x_center_approx, start_search_y, white_colors_rgb, color_tolerance=20, search_distance_lines=search_distance_lines_fixed, line_spacing=line_spacing_fixed, horizontal_check_offset=horizontal_check_offset_fixed)

    if popup_top != -1:
        final_popup_left = popup_left_fixed - 44
        final_popup_top = max(0, int(popup_top - top_padding_fixed))
        final_popup_right = popup_right_fixed - 44
        final_popup_bottom = min(screen_height, int(popup_bottom_est))
        return final_popup_left, final_popup_top, final_popup_right, final_popup_bottom
    else:
        return None

def capture_trait_popup(button_region, output_path="trait_popup.png"):
    try:
        boundaries = get_trait_popup_boundaries(button_region)
        if boundaries:
            left, top, right, bottom = boundaries
            popup_width = right - left
            popup_height = bottom - top

            if popup_width > 0 and popup_height > 0:
                screenshot = pyautogui.screenshot(region=(left, top, popup_width, popup_height))
                popup_image = screenshot.convert('RGB')

                top_padding = 8
                line_height_per_line = 30
                bottom_padding = 40
                text_area_height = popup_height - top_padding - bottom_padding
                num_lines = round(text_area_height / 30) if text_area_height > 0 else 0
                num_lines = max(1, num_lines)

                full_text = []
                for i in range(int(num_lines)):
                    line_y_start_relative = top_padding + i * line_height_per_line
                    line_y_end_relative = top_padding + (i + 1) * line_height_per_line

                    if line_y_end_relative <= popup_height - bottom_padding and line_y_start_relative >= top_padding:
                        line_region = (0, int(line_y_start_relative), popup_width, int(line_y_end_relative + 3))
                        cropped_line = popup_image.crop(line_region)
                        line_text = perform_ocr_single_line(cropped_line, debug=False, threshold=True)
                        if line_text:
                            full_text.append(line_text.strip())

                return " ".join(full_text).strip()
            else:
                print("Calculated popup dimensions are invalid.")
                return None
        else:
            print("Could not find the top of the popup text.")
            return None
    except Exception as e:
        print(f"Error in capture_trait_popup: {e}")
        return None

def process_trait(region, i):
    title_filename = f"trait_{i+1}.png"
    pyautogui.screenshot(title_filename, region=region)
    trait_title = None
    try:
        title_image = Image.open(title_filename)
        trait_title = perform_ocr(title_image, psm=7)
    except Exception as e:
        print(f"Error during title OCR: {e}")

    trait_region = (region[0], region[1], region[2], region[3])
    trait_text = capture_trait_popup(trait_region)
    trait_color = get_trait_color(region, UNIT_TRAIT_TARGET_COLORS_RGB, UNIT_TRAIT_COLOR_TOLERANCE)
    return {
        "trait title": trait_title,
        "trait text": trait_text,
        "trait color": trait_color,
        "modifiers": []
    }


def capture_unit_traits():
    captured_traits_data = []
    first_trait_attempt = True
    for i, region in enumerate(UNIT_TRAIT_POTENTIAL_REGIONS):
        trait_present = False

        if first_trait_attempt:
            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            move((center_x, center_y))
            first_trait_attempt = False
            trait_present = is_trait_present(region, UNIT_TRAIT_TARGET_COLORS_RGB, UNIT_TRAIT_COLOR_TOLERANCE)
            if trait_present:
                trait_data = process_trait(region, i)
                captured_traits_data.append(trait_data)
                move((center_x, center_y))
                time.sleep(0.05)

        else:
            trait_present = is_trait_present(region, UNIT_TRAIT_TARGET_COLORS_RGB, UNIT_TRAIT_COLOR_TOLERANCE)
            if trait_present:
                trait_data = process_trait(region, i)
                captured_traits_data.append(trait_data)
                center_x = region[0] + region[2] // 2
                center_y = region[1] + region[3] // 2
                move((center_x, center_y))
                time.sleep(0.05)

        if not trait_present and not first_trait_attempt:
            break

    return captured_traits_data

def find_white_text_top(start_x_center, start_y, white_colors, color_tolerance=20, search_distance_lines=10, line_spacing=30, horizontal_check_offset=5):
    screen_width, screen_height = pyautogui.size()
    top_y = start_y
    previous_top_y = start_y

    for i in range(1, search_distance_lines + 1):
        check_y = start_y - i * line_spacing
        if check_y < 0:
            break
        found_white_in_line_bottom = False
        for x_offset in range(-horizontal_check_offset, horizontal_check_offset + 1):
            check_x = start_x_center + x_offset
            if 0 <= check_x < screen_width and 0 <= check_y < screen_height:
                pixel_color = pyautogui.pixel(int(check_x), int(check_y))
                for white_color in white_colors:
                    if colors_are_similar(pixel_color, white_color, color_tolerance):
                        top_y = check_y
                        found_white_in_line_bottom = True
                        break
            if found_white_in_line_bottom:
                break

        if not found_white_in_line_bottom:
            return previous_top_y
        else:
            previous_top_y = top_y

    return top_y if top_y != start_y else -1

def get_text_lines(image, threshold_value=200): # We won't use threshold_value directly now
    """Identifies the vertical boundaries of text lines in an image using Otsu's method."""
    img_gray = image.convert('L')
    img_np = np.array(img_gray)
    _, thresh = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) # Using Otsu
    height, width = thresh.shape
    line_starts = []
    line_ends = []
    in_line = False

    for y in range(height):
        row = thresh[y, :]
        if np.any(row == 255) and not in_line:
            line_starts.append(y)
            in_line = True
        elif not np.any(row == 255) and in_line:
            line_ends.append(y)
            in_line = False

    if in_line: 
        line_ends.append(height)

    lines = []
    for start, end in zip(line_starts, line_ends):
        lines.append((0, start, image.width, end - start))  # (x, y, w, h)
    return lines, thresh