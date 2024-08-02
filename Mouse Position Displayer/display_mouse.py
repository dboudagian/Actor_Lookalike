import pyautogui
import time

try:
    while True:
        # Get the current mouse position
        x, y = pyautogui.position()
        # Clear the output and print the current mouse position
        print(f'X: {x} Y: {y}', end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nProgram exited")
