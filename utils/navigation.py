# navigation.py

import autoit, time

def move_and_click(coordinates):
    x, y = coordinates
    autoit.mouse_move(x, y)
    autoit.mouse_down("left")
    time.sleep(0.05)
    autoit.mouse_up("left")
    time.sleep(0.2)