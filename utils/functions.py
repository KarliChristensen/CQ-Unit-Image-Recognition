# functions.py

import pyautogui, json, autoit
from config import OUTPUT_JSON_FILES
from .navigation import move
from .ocr import perform_ocr_single_line

def capture_hover_popup(button_region, yellow_colors=None, title_color_hex="#9D9D9D", yellow_text_offset_up=25, yellow_text_offset_left=411):
    try:
        button_left, button_top, button_width, button_height = button_region
        title_color_rgb = hex_to_rgb(title_color_hex)

        if yellow_colors is None:
            yellow_colors_hex = ["#A69879", "#AA9B7C", "#95896D"]
            yellow_colors = [hex_to_rgb(hex_code) for hex_code in yellow_colors_hex]

        def is_yellow(rgb, yellow_colors_local):
            color_tolerance = 10
            for yellow in yellow_colors_local:
                if colors_are_similar(rgb, yellow, color_tolerance):
                    return True
            return False
        
        move(button_region)

        expected_yellow_text_x = button_left - yellow_text_offset_left
        expected_yellow_text_y_start = button_top - yellow_text_offset_up

        found_yellow = False
        yellow_text_x = -1
        yellow_text_y_start = -1
        for x_offset in range(-2, 2):
            for y_offset in range(-2, 2):
                sample_x = expected_yellow_text_x + x_offset
                sample_y = expected_yellow_text_y_start + y_offset
                if 0 <= sample_x < pyautogui.size()[0] and 0 <= sample_y < pyautogui.size()[1]:
                    pixel_color = pyautogui.pixel(int(sample_x), int(sample_y))
                    if is_yellow(pixel_color, yellow_colors):
                        yellow_text_x = sample_x
                        yellow_text_y_start = sample_y
                        found_yellow = True
                        break
            if found_yellow:
                break

        if found_yellow:
       
            title_top = -1
            for y in range(yellow_text_y_start - 5, max(0, yellow_text_y_start - 300), -1):
                pixel_color = pyautogui.pixel(int(yellow_text_x), int(y))
                if colors_are_similar(pixel_color, title_color_rgb, color_tolerance=5): 
                    title_top = y
                    break

            if title_top != -1:
                popup_left = yellow_text_x - 15 
                popup_top = title_top - 20
                popup_right = button_left
                popup_bottom = button_top

                final_popup_left = max(0, int(popup_left))
                final_popup_top = max(0, int(popup_top))
                final_popup_right = min(pyautogui.size()[0], int(popup_right))
                final_popup_bottom = min(pyautogui.size()[1], int(popup_bottom))

                final_popup_width = final_popup_right - final_popup_left
                final_popup_height = final_popup_bottom - final_popup_top

                title_box = (400, 29)
                text_box = (400, 24)
                translate = (24)

                # --- MODIFIED LINE ---
                text_content_height = final_popup_height - 100
                remainder = text_content_height % 23
                if remainder <= 23 / 2:
                    adjusted_text_height = text_content_height - remainder
                else:
                    adjusted_text_height = text_content_height + (23 - remainder)
                final_popup_height = adjusted_text_height + 100
                # --- MODIFIED LINE ---

                lines = int(adjusted_text_height / 23) + 1 if final_popup_height > 100 and 23 != 0 else 0

                captured_title = []
                captured_text = []

                title_region_coords = (final_popup_left + 4, final_popup_top, title_box[0], title_box[1])
                title_screenshot = pyautogui.screenshot(region=title_region_coords)
                title_text = perform_ocr_single_line(title_screenshot, debug=False, threshold=True, threshold_value=100)
                captured_title.append(title_text)

                for i in range(1, lines + 1):
                    text_y = final_popup_top + 30 + title_box[1] + (i - 1) * translate
                    current_text_region_coords = (final_popup_left + 4, text_y, text_box[0], text_box[1])
                    text_screenshot = pyautogui.screenshot(region=current_text_region_coords)
                    text_block = perform_ocr_single_line(text_screenshot, debug=False, threshold=True, threshold_value=100)
                    captured_text.append(text_block)

                extracted_title = " ".join(filter(None, captured_title)).strip()
                extracted_text = " ".join(filter(None, captured_text)).strip()

                if final_popup_width > 0 and final_popup_height > 0:
                    return extracted_title, extracted_text
                else:
                    return None
            else:
                return None
        else:
            return None

    except Exception as e:
        print(f"Error capturing dynamic hover pop-up (text-based - final - area scan): {e}")
        return None
    
def append_unit_to_json(unit_data):
    primary_type = unit_data.get('primary_type')
    if primary_type in OUTPUT_JSON_FILES:
        filename = OUTPUT_JSON_FILES[primary_type]
        try:
            with open(filename, 'r+') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        data.append(unit_data)
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                    else:
                        json.dump([unit_data], f, indent=4)
                except json.JSONDecodeError:
                    json.dump([unit_data], f, indent=4)
        except FileNotFoundError:
            with open(filename, 'w') as f:
                json.dump([unit_data], f, indent=4)
        print(f"Unit appended to '{filename}'")
    else:
        print(f"Warning: Unknown primary type '{primary_type}'. Unit not saved to a specific category file.")

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def is_button_present(region, grey_rgb, tolerance):
    x, y, w, h = region
    for offset_y in range(h - 4, h):
        sample_points = [x + w // 4, x + w // 2, x + 3 * w // 4]
        for sample_x in sample_points:
            pixel_color = autoit.pixel_get_color(sample_x, y + offset_y)
            r = (pixel_color >> 16) & 0xFF
            g = (pixel_color >> 8) & 0xFF
            b = pixel_color & 0xFF
            if abs(r - grey_rgb[0]) < tolerance and \
               abs(g - grey_rgb[1]) < tolerance and \
               abs(b - grey_rgb[2]) < tolerance:
                return True
    return False

def colors_are_similar(rgb1, rgb2, color_tolerance):
    return all(abs(c1 - c2) <= color_tolerance for c1, c2 in zip(rgb1, rgb2))