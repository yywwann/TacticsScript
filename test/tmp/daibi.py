import time
import pyautogui as auto

while True:
    auto.moveTo(1370, 370, duration=0.25)
    auto.dragTo(1370, 830, duration=0.25)

    auto.doubleClick(840, 480)
    time.sleep(3)

    auto.doubleClick(1048, 672)
    time.sleep(3)

    auto.doubleClick(1048, 835)
    time.sleep(3)




