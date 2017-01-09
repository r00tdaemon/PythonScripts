import sys
import argparse
import time

import pyautogui
import pyperclip
import win32api, win32con

pyautogui.PAUSE = 1.5

parser = argparse.ArgumentParser(description='Save opened tabs of your browser')

parser.add_argument('-P', '--open', action='store_true')
parser.add_argument('-i', '--input', default='a.txt')
parser.add_argument('-o', '--output', default='a.txt')
parser.add_argument('-b', '--browser', default='firefox', choices=['firefox', 'chrome'])
parser.add_argument('-p', '--open-now', action='store_true')


args = parser.parse_args(sys.argv[1:])
args = vars(args)

if args['browser'] == 'firefox':
    pointer_location = (660, 840)
else:
    pointer_location = (760, 840)
    
def isNumLockOn():
    "return 1 if NumLock is ON"
    return win32api.GetKeyState(win32con.VK_NUMLOCK)

def opennow(file):
    if args['browser'] == 'firefox':
        pyautogui.rightClick(pointer_location[0], pointer_location[1])
        time.sleep(1)
        pyautogui.click(650, 720)
        pyautogui.press('f6')
    else:
        pyautogui.hotkey('winleft', 's')
        pyautogui.typewrite('chrome')
        pyautogui.hotkey('apps')
        if isNumLockOn():
            pyautogui.press('numlock')
        pyautogui.press('up')
        pyautogui.press('enter')
    with open(file) as input_file:
        for tab in input_file.readlines():
            pyautogui.typewrite(tab)
            pyautogui.hotkey('ctrl', 't')
        pyautogui.hotkey('ctrl', 'w')


if args['open']:
    opennow(args['input'])
    exit(0)

pyautogui.click(pointer_location[0], pointer_location[1])
tabs = []
while True:
    pyautogui.press('f6')
    pyautogui.hotkey('ctrl', 'c')
    if pyperclip.paste() in tabs:
        break
    tabs.append(pyperclip.paste())
    pyautogui.hotkey('ctrl', 'tab')

with open(args['output'], 'w') as output:
    for tab in tabs:
        output.write(str(tab) + '\n')

if args['open_now']:
    pyautogui.hotkey('alt', 'f4')
    pyautogui.press('enter')
    opennow(args['output'])