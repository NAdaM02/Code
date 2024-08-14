import pyautogui
import cv2
import csv
import numpy as np
import time
from time import sleep as wait
from time import time as now
import random
import sys
import os
import screeninfo
from PIL import ImageGrab
import pygetwindow as gw



#
# imports
#
#
#
#
#
#
# values
#


question_num = 9
ans_list = [2, 4, 4, 1, 4, 1, 3, 3, 2]



Monitors = screeninfo.get_monitors()
selected_monitor = Monitors[0]

window = gw.getWindowsWithTitle("Firefox")[0]
window_rect = (window.left, window.top, window.right, window.bottom)
window_center = ( (window.left + window.right)/2, (window.top + window.bottom)/2 )


dot = (os.path.dirname(__file__)).replace('\\','/')

time_convert_list = (29030400, 604800, 86400, 3600, 60, 1)
time_char_list = ('y', 'w', 'd', 'h', 'm', 's')

order = [i for i in range(2, question_num)]+[1]

with open(f'{dot}/Data/threshes.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    threshes = {}
    for row in reader:
        if row['img'] != '' and row['img'] != '.' and row['img'] != '...':
            try:
                threshes = threshes | {row['img']:float(row['thresh'])}
            except:
                threshes = threshes | {row['img']:0.0}

with open( f'{dot}/Data/question_vals.txt', 'r') as question_vals_file:
    question_vals = list(map(float,question_vals_file.read().split(' | ')))



#
# values
#
#
#
#
#
#
# functions
#



def findImageOnScreen(img_to_detect:str, threshold:float='', screen_index:int=0, memory:bool=False) :
    global last_val, selected_monitor, window_rect

    img_to_detect_path = f'{dot}/Pics/{img_to_detect}.png'
    if threshold == '':
        threshold = threshes[img_to_detect]

    template = cv2.imread(img_to_detect_path, cv2.IMREAD_GRAYSCALE)
    template_height, template_width = template.shape[:2]

    screenshot = ImageGrab.grab(window_rect)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if memory == True:
        last_val = max_val
    if max_val >= threshold-0.05:
        center_x = max_loc[0] + selected_monitor.x + template_width // 2
        center_y = max_loc[1] + selected_monitor.y + template_height // 2
        return (center_x, center_y)
    else:
        return None



def writeByLetter(string:str, delay:float=0.1) :
    for l in range(len(string)-1):
        sys.stdout.write(string[l])
        sys.stdout.flush()
        wait(delay*(random.random()+0.5) * (1 if string[l+1] != string[l] else 3 ))
    sys.stdout.write(string[-1])
    sys.stdout.flush()
    print('')



def selectAnswer(i:int) :
    global ans_list, window, window_center, found
    template = cv2.imread(f'{dot}/Pics/a{i+1}.png', cv2.IMREAD_GRAYSCALE)
    template_height, template_width = template.shape[:2]
    ans_height = template_height * 23 / 111
    blank_space = template_height * 5 / 74
    place = i
    mistake = False
    if mistake_rate != 0:
        mistake = ( random.randint(1, mistake_rate) == 1 )
        if mistake:
            place = random.randint(1,4)
            while place == i:
                place = random.randint(1,4)
        else:
            place = ans_list[i]
    box = False
    while not box:
        box = findImageOnScreen(f'a{i+1}', threshold=0)
    yx = int(box[1] - template_height / 2 + ans_height / 2 + (place - 1) * (ans_height + blank_space))
    wait(0.1)
    pyautogui.click(x=found[0], y=yx)
    wait(0.1)
    pyautogui.click(x=window.right-10, y=window.bottom-10)
    #pyautogui.moveTo(x=window.right+5, y=window.bottom+5)


    return f"_{place}" if mistake else f"{ans_list[i]} "



def secs_to_text(seconds:float) :
    seconds = int(seconds)
    text = ""
    for i in range(len(time_convert_list)):
        conv = time_convert_list[i]
        if conv <= seconds:
            un = seconds//conv
            seconds -= un*conv
            text += str(un) + time_char_list[i] + " "
    text = f'{text}\b'
    return text
        
def text_to_secs(text:str) :
    ls = text.split()
    secs = 0
    for v in ls:
        try:
            secs += time_convert_list[time_char_list.index(v[-1])]*int("".join(v[:-1]))
        except:
            return False
    return secs



def getQuestion(devs_mode:bool=False):
    global window_rect, question_vals
    screenshot = ImageGrab.grab(window_rect)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    val = np.average(screenshot)
    devs = [abs(question_val-val) for question_val in question_vals]

    if not devs_mode :
        min_d = devs[0]
        min_i = 0

        for i in range(1, len(devs)):
            if devs[i] < min_d :
                min_d = devs[i]
                min_i = i
        
        return val, min_i
    
    else:
        return devs



solved = []
def solveQuestion():
    global solved, found
    devs = getQuestion(devs_mode=True)
    order = sorted(range(len(devs)), key=lambda x: devs[x])
    for i in order:
        if i not in solved:
            print(f"\b{i+1}", end="")
            sys.stdout.flush()
            found = findImageOnScreen(f'q{i+1}')
            
            if found:
                """gqv, gqi = getQuestion()
                question_vals[i] = gqv
                with open( f'{dot}/Data/question_vals.txt', 'w') as question_vals_file:
                    question_vals_file.write(' | '.join(list(map(str,question_vals))))"""
                m = selectAnswer(i)
                solved.append(i)
                print(f"->{m}   ",end="") if len(solved) != 6 else print(f"->{m}",end="")
                sys.stdout.flush()

                break
        """print(f"\b_", end="")

        while i == last_i :
            v, i = getQuestion()
        last_i = i

        print(f"\b{i+1}", end="")
        sys.stdout.flush()
        m = selectAnswer(i)
        found_t = True
        solved.append(i)
        print(f"->{m}   ",end="")
        sys.stdout.flush()"""



#
# functions
#
#
#
#
#
#
# M A I N
#



if __name__ == "__main__" :
    print()
    writeByLetter('### AlphaGames Bot ###',0.08)
    print()
    print()

    goal = input('Set goal _ ')
    time_goal = text_to_secs(goal)
    if time_goal:
        mode = "time"
        time_goal_text = goal
        goal = 0
    else:
        mode = "goal"
        goal = int(goal)
        time_goal = 0

    mistake_rate = input('mistake rate [21] : ')
    mistake_rate = int(mistake_rate) if mistake_rate != '' and mistake_rate != '\n' else 21
    
    difficulty = input('difficulty [medium] : ')
    difficulty = difficulty if difficulty != '' and difficulty != '\n' else 'medium'

    print()
    print()
    writeByLetter('Program starting...')
    sys.stdout.write('- ')
    wait(1)
    print('now\n')

    loss_count = 0
    _sum = 0
    task_durations = []
    ran = 0
    ETAs = []
    start_time = now()

    while (mode == "goal" and _sum < goal) or (mode == "time" and (now() - start_time) < time_goal):
        ran += 1
        start = now()

        wait(0.2)

        if difficulty == 'hard' or difficulty == 'h' :
            found_hard = False
            while not found_hard:
                found_hard = findImageOnScreen('hard')
            wait(0.1)
            pyautogui.click(x=found_hard[0], y=found_hard[1])

            wait(0.1)
            pyautogui.moveTo(x=window.right+1, y=window.bottom+1)
        elif difficulty == 'medium' or difficulty == 'm' :
            found_medium = False
            while not found_medium:
                found_medium = findImageOnScreen('medium')
            wait(0.1)
            pyautogui.click(x=found_medium[0], y=found_medium[1])

            wait(0.1)
            pyautogui.moveTo(x=window.right+1, y=window.bottom+1)

        found_start = False
        while not found_start :
            found_start = findImageOnScreen('start')
        pyautogui.click(x=found_start[0], y=found_start[1])
        wait(0.1)
        pyautogui.click(x=window.right-10, y=window.bottom-10)

        found_start = False
        found_start_n = False
        found_start_for = 0
        found_start_time = 0

        found_l = False
        found_l_n = False
        found_l_for = 0
        found_l_time = 0
        while found_l_for <= 0.1 :
            found_l_n = findImageOnScreen('l')
            if not found_l :
                found_l_for = 0
                if found_l_n :
                    found_l_for = 0
            else:
                found_l_for += time.perf_counter() - found_l_time
            found_l = found_l_n
            if found_l:
                found_l_time = time.perf_counter()
            
            found_start_n = findImageOnScreen('start')
            if not found_start :
                found_start_for = 0
                if found_start_n :
                    found_start_for = 0
            else:
                found_start_for += time.perf_counter() - found_start_time
            found_start = found_start_n
            if found_start:
                found_start_time = time.perf_counter()

            if found_start_for >= 1.2 and found_start :
                pyautogui.click(x=found_start[0], y=found_start[1])
                wait(0.1)
                pyautogui.click(x=window.right-10, y=window.bottom-10)
                found_start = False

        print(f'{ran}:'+" "*(6-len(str(ran))),end="")
        sys.stdout.flush()
        

        solved = []
        quests_start = now()
        while len(solved) < 6 : # len(solved) < 6 and now() - quests_start < 30
            solveQuestion()
            if now() - quests_start >= 15:
                while not findImageOnScreen('new') :
                    solved = []
                    solveQuestion()
                break

        wait(1.5)
        print('\b')
        sys.stdout.flush()

        score = 0
        while score == 0:
            if findImageOnScreen('p4'):
                score = +4
            elif findImageOnScreen('p8'):
                score = +8
            elif findImageOnScreen('m4'):
                score = -4
                loss_count += 1
            elif findImageOnScreen('m1'):
                score = -1
                loss_count += 1
            elif findImageOnScreen('p14', threshold=1):
                score = +14
            elif findImageOnScreen('p6', threshold=1):
                score = +6
        _sum += score

        print(f"|| {score}" if score < 0 else f"|| +{score}")

        if mode == "goal" :
            ETA = int( (now() - start_time) * (goal/_sum - 1) ) if not _sum == 0 and _sum < goal else 0
            if ETA > 0:
                ETAs.append(ETA)
            ETA_text = secs_to_text(ETA)

            percentage = int(_sum/goal*1000)/10

            print( f"Sum = {_sum}" + " "*(8-len(str(_sum))) + f"ETA: {ETA_text}" + " "*(18-len(ETA_text)) + f"{percentage}%" )

        elif mode == "time" :
            percentage = int( (now() - start_time)/time_goal*1000 )/10

            passed_secs = now() - start_time
            rate = _sum / passed_secs
            expected_sum = rate * time_goal
            remaining_secs = time_goal - now() + start_time

            remaining_text = secs_to_text(remaining_secs)
            print( f"Sum = {_sum}" + " "*(8-len(str(_sum))) + f"rem: {remaining_text}" + " "*(18-len(remaining_text)) + f"expSum: {int(round(expected_sum,0))}" )

        print()

        # new game
        found_new = False
        while not found_new:
            found_new = findImageOnScreen('new')
        wait(0.1)
        while found_new:
            pyautogui.click(x=found_new[0], y=found_new[1])
            wait(0.1)
            pyautogui.moveTo(x=window.right+1, y=window.bottom+1)
            found_new = findImageOnScreen('new')

        task_durations.append(now() - start)
        # repeat


    runtime = now() - start_time
    runtime_text = secs_to_text(runtime)
    print()
    
    if mode == "goal":
        writeByLetter(f"> Reached goal ({_sum})" if _sum == goal else f"> Reached goal ({goal}+{_sum-goal})")
    elif mode == "time":
        writeByLetter(f"> Reached time ({time_goal_text})" if time_goal == runtime else f"> Reached time ({time_goal_text} + {secs_to_text(runtime-time_goal)})")
        print(f"Points gathered: {_sum}")

    print()
    writeByLetter("(Elapsed)")
    print(runtime_text)

    if mode == "goal":
        avg_ETA = sum(ETAs)/len(ETAs)*2
        avg_ETA_text = secs_to_text(avg_ETA)
        writeByLetter("(Average ETA)")
        print(avg_ETA_text)
    print()
    writeByLetter("> Program paused")



#
# M A I N
#
#
#
#
#
#
#
#


