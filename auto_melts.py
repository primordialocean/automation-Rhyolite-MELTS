import subprocess
import pyautogui
import os
import time
import json

from pyscreeze import ImageNotFoundException
import pyscreeze
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = True

def get_filenames(directory, extension):
    filenames = []
    for file in os.listdir(directory):
        if file.endswith(extension):
            filename_wo_extension = os.path.splitext(file)[0]
            filenames.append(filename_wo_extension)
    return filenames

def click_point(imgname):
    position = pyautogui.locateOnScreen("img/"+imgname, confidence=0.95)
    pyautogui.click(position)

def move_results(filename):
    subprocess.run("mkdir out/"+filename, shell=True)
    subprocess.run("mv *.inp out/"+filename+"/", shell=True)
    subprocess.run("mv *.tbl out/"+filename+"/", shell=True)
    subprocess.run("mv *.out out/"+filename+"/", shell=True)

def calc_melts(dt, filename):
    subprocess.run(
        "echo 'y\nn\ny\n' | ./Melts-rhyolite-public ./melts_mv.sh &",
        shell=True)
    
    for trycount in range(10001):
        if trycount < 10000:
            try:
                click_point("melts120_title.png")
                pyautogui.hotkey("ctrl", "o")
                time.sleep(2)
                position = pyautogui.locateOnScreen("img/fileselection.png", confidence=0.95)
            except pyautogui.ImageNotFoundException:
                time.sleep(1)
            else:
                time.sleep(1)
                pyautogui.click(position)
                break
        else:
            sys.exit()
    pyautogui.write("in/"+filename+".melts", interval = 0.1)
    pyautogui.press("enter")
    pyautogui.hotkey("ctrl", "e")
    time.sleep(dt)
    
    for trycount in range(11):
        if trycount < 10:
            try:
                click_point("melts120_title.png")
                pyautogui.hotkey("ctrl", "c")
                time.sleep(1)
                click_point("warning_message.png")
            except pyautogui.ImageNotFoundException:
                time.sleep(1)
            else:
                pyautogui.hotkey("left")
                time.sleep(1)
                pyautogui.hotkey("enter")
                break
        else:
            subprocess.run('pgrep "Melts-rhyolite" | xargs kill', shell=True)

    time.sleep(1)
    move_results(filename)

def main():
    # load config.json
    with open("config.json") as f:
        config = json.load(f)
    
    config_tmp = config["auto_melts"]
    dt_s = config_tmp["Interval time (s)"]
    
    filenames = get_filenames("./in", ".melts")

    count = 0
    for filename in filenames:
        calc_melts(dt_s, filename)
        count += 1
        print(filename)
        print(str(int(100 * count / len(filenames)))+"%")

if __name__ == '__main__':
    main()
