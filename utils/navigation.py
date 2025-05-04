import autoit
import time

def move_and_click(coordinates):
    try:
        if len(coordinates) == 4:
            x, y, width, height = coordinates
            center_x = x + width // 2
            center_y = y + height // 2
        elif len(coordinates) == 2:
            center_x, center_y = coordinates
        else:
            raise ValueError("Coordinates must be a tuple or list of two or four numbers.")
    except TypeError:
        raise ValueError("Coordinates must be a tuple or list.")
    except ValueError as e:
        raise e  # Re-raise the ValueError with the specific message
    autoit.mouse_move(center_x, center_y)
    autoit.mouse_down("left")
    time.sleep(0.05)
    autoit.mouse_up("left")
    time.sleep(0.05)

def move(coordinates):
    try:
        if len(coordinates) == 4:
            x, y, width, height = coordinates
            center_x = x + width // 2
            center_y = y + height // 2
        elif len(coordinates) == 2:
            center_x, center_y = coordinates
        else:
            raise ValueError("Coordinates must be a tuple or list of two or four numbers.")
    except TypeError:
        raise ValueError("Coordinates must be a tuple or list.")
    except ValueError as e:
        raise e  # Re-raise the ValueError with the specific message
    time.sleep(0.05)
    autoit.mouse_move(center_x, center_y)
    time.sleep(0.05)