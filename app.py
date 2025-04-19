import pyautogui

def capture_full_screenshot(filename="full_screenshot.png"):
    """Captures a full-screen screenshot and saves it to the specified filename."""
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Full-screen screenshot saved as {filename}")
        return True
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return False

if __name__ == "__main__":
    capture_full_screenshot()