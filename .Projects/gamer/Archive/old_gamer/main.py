import pyautogui
import cv2
import numpy as np
import time
from time import sleep as wait
import random
import sys
from screeninfo import get_monitors
import os
from PIL import ImageGrab



dot = (os.path.dirname(__file__)).replace('\\','/')

selected_monitor = get_monitors()[0]

question_num = 9

t_pics = [(dot+'/Pics/t'+str(i)+'.png') for i in range(1,question_num+1)]
q_pics = [(dot+'/Pics/q'+str(i)+'.png') for i in range(1,question_num+1)]

ans_list = [2, 4, 4, 1, 4, 1, 3, 3, 2]

threshes = [0.86, 0.86, 0.76, 0.76, 0.86, 0.84, 0.76, 0.73, 0.79]

order = [i for i in range(1, question_num)]+[0]

time_convert_list = (29030400, 604800, 86400, 3600, 60, 1)
time_char_list = ('y', 'w', 'd', 'h', 'm', 's')




def findImageOnScreen(img_to_detect_path:str, screen_index:int=0, threshold:float=0.78, memory:bool=False) :
    global last_val
    template = cv2.imread(img_to_detect_path, cv2.IMREAD_GRAYSCALE)
    template_height, template_width = template.shape[:2]

    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if memory == True:
        last_val = max_val
    if max_val >= threshold:
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
    global q_pics, ans_list, threshes
    template = cv2.imread(q_pics[i], cv2.IMREAD_GRAYSCALE)
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
    box = False
    while not box:
        box = findImageOnScreen(q_pics[i], threshold=0.8)
    if mistake:
        yx = int(box[1] - template_height / 2 + ans_height / 2 + (place - 1) * (ans_height + blank_space))
    else:
        yx = int(box[1] - template_height / 2 + ans_height / 2 + (ans_list[i] - 1) * (ans_height + blank_space))
    wait(0.1)
    pyautogui.click(x=found[0], y=yx)
    wait(0.1)
    pyautogui.moveTo(x=found[0] + template_width / 20 * 11, y=box[1])

    return f"!{place}" if mistake else f"{ans_list[i]} "



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
    start_time = time.time()

    while (mode == "goal" and _sum < goal) or (mode == "time" and (time.time() - start_time) < time_goal):
        ran += 1
        start = time.time()

        wait(0.2)

        if difficulty == 'hard' or difficulty == 'h' :
            found_hard = False
            while not found_hard:
                found_hard = findImageOnScreen((f'{dot}/Pics/hard.png'))
            wait(0.1)
            pyautogui.click(x=found_hard[0], y=found_hard[1])

            wait(0.1)
        elif difficulty == 'medium' or difficulty == 'm' :
            found_medium = False
            while not found_medium:
                found_medium = findImageOnScreen((f'{dot}/Pics/medium.png'))
            wait(0.1)
            pyautogui.click(x=found_medium[0], y=found_medium[1])

            wait(0.1)

        found_start = False
        while not found_start :
            found_start = findImageOnScreen(f'{dot}/Pics/start.png', threshold=0.97)
        pyautogui.click(x=found_start[0], y=found_start[1])
        wait(0.1)
        pyautogui.moveTo(x=found_start[0]+100, y=found_start[1])

        found_start = False
        found_start_n = False
        found_start_for = 0
        found_start_time = 0

        found_l = False
        found_l_n = False
        found_l_for = 0
        found_l_time = 0
        while found_l_for <= 0.1 :
            found_l_n = findImageOnScreen(f'{dot}/Pics/l.png', threshold=0.98)
            if not found_l :
                found_l_for = 0
                if found_l_n :
                    found_l_for = 0
            else:
                found_l_for += time.perf_counter() - found_l_time
            found_l = found_l_n
            if found_l:
                found_l_time = time.perf_counter()
            
            found_start_n = findImageOnScreen(f'{dot}/Pics/start.png', threshold=0.97)
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
                pyautogui.moveTo(x=found_start[0]+100, y=found_start[1])
                found_start = False

        print(f'{ran}:'+" "*(4-len(str(ran))),end="")
        sys.stdout.flush()
        solved = []
        while len(solved) < 6 :
            found_t = False
            while not found_t:
                for i in order: # i = [1, 2 ... q_num-1, 0]
                    if i not in solved:
                        print(f"\b{i+1}", end="")
                        sys.stdout.flush()
                        found = findImageOnScreen(t_pics[i],threshold=threshes[i])
                        if found:
                            m = selectAnswer(i)
                            found_t = True
                            solved.append(i)
                            print(f"->{m}   ",end="")
                            sys.stdout.flush()
                            break

        print('\b')
        sys.stdout.flush()

        score = 0
        while score == 0:
            if findImageOnScreen(f'{dot}/Pics/+8.png', threshold=0.97):
                score = +8
            elif findImageOnScreen(f'{dot}/Pics/+4.png', threshold=0.93):
                score = +4
            elif findImageOnScreen(f'{dot}/Pics/-4.png', threshold=0.91):
                score = -4
                loss_count += 1
            elif findImageOnScreen(f'{dot}/Pics/+14.png', threshold=0.95):
                score = +14
            elif findImageOnScreen(f'{dot}/Pics/+6.png', threshold=0.94):
                score = +6
        _sum += score

        print(f"|| {score}" if score < 0 else f"|| +{score}")

        if mode == "goal" :
            ETA = int( (time.time() - start_time) * (goal/_sum - 1) ) if not _sum == 0 and _sum < goal else 0
            if ETA > 0:
                ETAs.append(ETA)
            ETA_text = secs_to_text(ETA)

            percentage = int(_sum/goal*1000)/10

            print( f"Sum = {_sum}" + " "*(8-len(str(_sum))) + f"ETA: {ETA_text}" + " "*(18-len(ETA_text)) + f"{percentage}%" )

        elif mode == "time" :
            percentage = int( (time.time() - start_time)/time_goal*1000 )/10

            remaining_text = secs_to_text(time_goal - time.time() + start_time)
            print( f"Sum = {_sum}" + " "*(8-len(str(_sum))) + f"rem: {remaining_text}" + " "*(18-len(remaining_text)) + f"{percentage}%" )

        print()

        # new game
        found_new = False
        while not found_new:
            found_new = findImageOnScreen(f'{dot}/Pics/new.png', threshold=0.91)
        wait(0.1)
        while found_new:
            pyautogui.click(x=found_new[0], y=found_new[1])
            wait(0.1)
            pyautogui.moveTo(x=found_new[0]+100, y=found_new[1])
            found_new = findImageOnScreen(f'{dot}/Pics/new.png')

        task_durations.append(time.time() - start)
        # repeat


    runtime = time.time() - start_time
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
