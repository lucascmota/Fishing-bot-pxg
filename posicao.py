
import pyautogui
import time



while True:
    x, y = pyautogui.position()
    time.sleep(2)
    screenshot = pyautogui.screenshot()
    cor = screenshot.getpixel((x, y))
    print(x, y, cor)
