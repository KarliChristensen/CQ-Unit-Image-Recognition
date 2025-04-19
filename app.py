import pyautogui

def capture_full_screenshot(filename="full_screenshot.png"):
    """Captures a full-screen screenshot and saves it."""
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Full-screen screenshot saved as {filename}")
        return True
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return False

def on_hotkey():
    """Function to be executed when the hotkey is pressed."""
    print("Hotkey detected! Capturing screenshot...")
    capture_full_screenshot()
    print("Screenshot captured and saved.")

if __name__ == "__main__":
    print("Press Ctrl+E to capture a full-screen screenshot.")
    pyautogui.hotkey('ctrl', 'e', callback=on_hotkey)
    pyautogui.PAUSE = 0.1  # Optional: Add a small pause for stability
    try:
        while True:
            pyautogui.sleep(1)  # Keep the script running to listen for hotkeys
    except KeyboardInterrupt:
        print("\nHotkey listener stopped.")