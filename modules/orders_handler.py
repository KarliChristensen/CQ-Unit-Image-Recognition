# orders_handler.py

import pyautogui
from config import ORDERS_POTENTIAL_REGIONS, BOX_COLOR_TOLERANCE, BOX_GREY_RGB
from utils.functions import is_button_present, capture_hover_popup
from utils.navigation import move

def capture_unit_orders():
    captured_orders = []
    for i, region in enumerate(ORDERS_POTENTIAL_REGIONS):
        if is_button_present(region, BOX_GREY_RGB, BOX_COLOR_TOLERANCE):
            orders_data = process_formation(region, i)
            captured_orders.append(orders_data)
            move(region)           
        else:
            break
    return captured_orders

def process_formation(region, i):
    filename = f"orders_icon_{i+1}.png"
    pyautogui.screenshot(filename, region=region)
    title, text = capture_hover_popup(region)
    print(f"Extracted title: {title}")
    print(f"Extracted text: {text}")

    return {
        "formation title": title,
        "formation text": text,
        "modifiers": []
    }