import win32api, win32con
import keyboard
import time
import cv2
from PIL import ImageGrab
from PIL import Image
import numpy as np
import sys
import os

show = False

#bbox defaults (game area on my screen)
x1 = 1281
y1 = 128
x2 = 2537
y2 = 660

continue_btn = (1900, 536)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

numbers = []

#load images fron /Numbers/
for i in range(len(os.listdir('./numbers/'))):
    numbers.append(cv2.imread(f'./numbers/{i+1}.png', 1))

keyboard.wait('enter')

while True:
    screen_shot = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
    
    #positions to click
    number_positions = []

    for i in range(len(numbers)):
        number = numbers[i]

        result = cv2.matchTemplate(screen_shot, number, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        print(i + 1, max_loc, '|', max_val)
        
        #if found
        if max_val > 0.5:
            #append position
            number_positions.append(max_loc)
            
            #draw clicking pos to screenshot
            cv2.putText(screen_shot, str(i + 1),
                max_loc,
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2)

    if show:
        img_pil = Image.fromarray(screen_shot)
        img_pil.show()
        keyboard.wait('enter')
    
    #click numbers in order
    for number in number_positions:
        click(x1 + number[0], y1 + number[1])
        time.sleep(0.1)
    
    #click continue
    click(continue_btn[0], continue_btn[1])

    keyboard.wait('enter')
