# functions.py

import pyautogui, time, json, autoit
from config import OUTPUT_JSON_FILES

def capture_hover_popup(button_region, output_path="dynamic_popup.png", yellow_colors=None, title_color_hex="#9D9D9D", yellow_text_offset_up=25, yellow_text_offset_left=411):
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

        center_x = button_left + button_width // 2
        center_y = button_top + button_height // 2
        pyautogui.moveTo(center_x, center_y)
        time.sleep(0.05)

        # Calculate potential start of the last yellow text line
        expected_yellow_text_x = button_left - yellow_text_offset_left
        expected_yellow_text_y_start = button_top - yellow_text_offset_up

        # Search for the yellow text in a small area
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
            # Scan upwards for the title color from the found yellow text position
            title_top = -1
            for y in range(yellow_text_y_start - 5, max(0, yellow_text_y_start - 300), -1): # Scan upwards
                pixel_color = pyautogui.pixel(int(yellow_text_x), int(y))
                if colors_are_similar(pixel_color, title_color_rgb, color_tolerance=5): # Adjust tolerance as needed
                    title_top = y
                    break

            if title_top != -1:
                # Define the pop-up region with final adjustments
                popup_left = yellow_text_x - 5 - 10 # Add 10 pixels to the left
                popup_top = title_top - 5 - 10 # Add 10 pixels to the top
                popup_right = button_left # Use the left side of the hovered button as the right
                popup_bottom = button_top # Use the top of the hovered button as the bottom

                final_popup_left = max(0, int(popup_left))
                final_popup_top = max(0, int(popup_top))
                final_popup_right = min(pyautogui.size()[0], int(popup_right))
                final_popup_bottom = min(pyautogui.size()[1], int(popup_bottom))

                final_popup_width = final_popup_right - final_popup_left
                final_popup_height = final_popup_bottom - final_popup_top

                if final_popup_width > 0 and final_popup_height > 0:
                    screenshot = pyautogui.screenshot(region=(final_popup_left, final_popup_top, final_popup_width, final_popup_height))
                    screenshot.save(output_path)
                    return output_path
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

def colors_are_similar(rgb1, rgb2, color_tolerance):
    return all(abs(c1 - c2) <= color_tolerance for c1, c2 in zip(rgb1, rgb2))

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

def is_trait_present(region, target_colors_rgb, tolerance):
    x, y, w, h = region
    bracket_offset_x = 48
    bracket_offset_y = 14

    sample_x = x + bracket_offset_x
    sample_y = y + bracket_offset_y

    pixel_color = autoit.pixel_get_color(sample_x, sample_y)
    r = (pixel_color >> 16) & 0xFF
    g = (pixel_color >> 8) & 0xFF
    b = pixel_color & 0xFF
    current_rgb = (r, g, b)

    for target_color in target_colors_rgb:
        if all(abs(current - target) < tolerance for current, target in zip(current_rgb, target_color)):
            return True
    return False

def _find_white_text_top(start_x_center, start_y, white_colors, color_tolerance=20, search_distance_lines=10, line_spacing=30, horizontal_check_offset=5):

    screen_width, screen_height = pyautogui.size()
    top_y = start_y # Initialize top_y with the starting y (bottom line)
    previous_top_y = start_y # Keep track of the last y where white text was found

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
                    break # Found white in this line, move to the next line up

        if not found_white_in_line_bottom:
            return previous_top_y # No white text found on this line, return the previous top_y
        else:
            previous_top_y = top_y # Update the previous top_y if white text was found

    return top_y if top_y != start_y else -1 # Return the topmost y found, or -1 if none found above the start

def capture_trait_popup(button_region, output_path="trait_popup.png"):
    try:
        button_left, button_top, button_width, button_height = button_region
        screen_width, screen_height = pyautogui.size()
        white_colors_hex = ["#8C8C8C", "#6B6B6C", "#CDCDCD", "#454546"]
        white_colors_rgb = [hex_to_rgb(hex_code) for hex_code in white_colors_hex]
        bottom_line_offset_fixed = 58
        text_block_x_offset_fixed = 1795 + 10 # Fixed left x + some padding (approximate start)
        line_spacing_fixed = 30
        popup_left_fixed = 1785
        popup_right_fixed = 2143
        popup_bottom_est = button_top - 36
        search_distance_lines_fixed = 10
        horizontal_check_offset_fixed = 5
        top_padding_fixed = 25 # Padding to add to the top

        center_x = button_left + button_width // 2
        center_y = button_top + button_height // 2
        pyautogui.moveTo(center_x, center_y)
        time.sleep(0.05)

        # Calculate the starting y-position for the bottom line search
        start_search_y = max(0, int(popup_bottom_est - bottom_line_offset_fixed))

        # Approximate the starting x-coordinate of the text block
        start_x_center_approx = int(text_block_x_offset_fixed + 10) # Add a bit to get closer to text

        # Scan upwards line by line to find the top of the white text block
        popup_top = _find_white_text_top(start_x_center_approx, start_search_y, white_colors_rgb, color_tolerance=20, search_distance_lines=search_distance_lines_fixed, line_spacing=line_spacing_fixed, horizontal_check_offset=horizontal_check_offset_fixed)

        if popup_top != -1:
            final_popup_left = popup_left_fixed
            final_popup_top = max(0, int(popup_top - top_padding_fixed)) # Apply the top padding
            final_popup_right = popup_right_fixed
            final_popup_bottom = min(screen_height, int(popup_bottom_est))

            final_popup_width = final_popup_right - final_popup_left
            final_popup_height = final_popup_bottom - final_popup_top

            if final_popup_width > 0 and final_popup_height > 0:
                screenshot = pyautogui.screenshot(region=(final_popup_left, final_popup_top, final_popup_width, final_popup_height))
                screenshot.save(output_path)
                return output_path
            else:
                return None
        else:
            return None

    except Exception as e:
        return None