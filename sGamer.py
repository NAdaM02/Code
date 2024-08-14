from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep as wait_seconds
from time import time as now
import os
import sys
import random


DOT = (os.path.dirname(__file__)).replace('\\','/')

TIME_CONVERT_LIST = (29030400, 604800, 86400, 3600, 60, 1)
TIME_CHAR_LIST = ('y', 'w', 'd', 'h', 'm', 's')

ADAM_USERNAME = 'adam.ancsin1@gmail.com'
ADAM_PASSWORD = 'HarsaG92'

JIMMY_USERNAME = 'Jimmalma1214@gmail.com'
JIMMY_PASSWORD = 'Jimmy1214'


#################################################################################################

XPATHS = {
    'username_input_field' : '/html/body/div/div[1]/div/div[1]/input',
    'password_input_field' : '/html/body/div/div[1]/div/div[2]/input',
    'login_button' : '/html/body/div/div[1]/div/button',
    'remember_me_checkbox' : '//*[@id=\'customCheck1\']',

    'games_section_button' : '/html/body/div/header/div/div/div/div[1]/nav/ul/li[2]/a',
    
    'medium_difficulty_button' : '/html/body/div/div[1]/div[1]/div[1]/button[2]'
}

OUTER_HTMLS = {
    'username_input_field' : '<input type="email" class="mt-1 p-2 w-full border rounded-md" placeholder="Add meg az email címed" value="">',
    'password_input_field' : '<input type="password" class="mt-1 p-2 w-full border rounded-md" placeholder="Írd be a jelszavad" value="">',
    'login_button' : '<button type="button" class="w-full py-2 px-4 bg-blue-500 text-white rounded-md hover:bg-blue-600">Bejelentkezés</button>',
    'remember_me_checkbox' : '<input type="checkbox" class="form-checkbox" id="customCheck1">',

    'games_section_button' : '<a href="/games" class="flex items-center">Játékok</a>',
    
    'medium_difficulty_button' : '<button class="text-xl font-bold py-2 px-4 rounded bg-green-200 transition duration-300 ease-in-out transform hover:-translate-y-1">Közepes</button>',
    'hard_difficulty_button' : '<button class="text-xl font-bold py-2 px-4 rounded bg-gray-200 transition duration-300 ease-in-out transform hover:-translate-y-1">Nehéz</button>',

    'start_game_button' : '<button class="btn btn-primary hover:bg-blue-400 text-white font-bold py-2 px-4 rounded">Játék indítása</button>'
}

CSS_SELECTORS = {
    'username_input_field' : 'div.mb-4:nth-child(2) > input:nth-child(2)',
    'password_input_field' : 'div.mb-4:nth-child(3) > input:nth-child(2)',
    'remember_me_checkbox' : '#customCheck1',
    'login_button' : 'button.w-full',

    'logout_button' : '.header-nav > button:nth-child(2)',
    'games_section_button' : '.navigation > nav:nth-child(1) > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)',
    
    'medium_difficulty_button' : 'button.text-xl:nth-child(2)',
    'hard_difficulty_button' : 'button.text-xl:nth-child(3)',
    'start_game_button' : 'div.bg-white:nth-child(2) > button:nth-child(5)',

    'score_text' : '.navigation > nav:nth-child(1) > ul:nth-child(1) > li:nth-child(6) > a:nth-child(1) > div:nth-child(1)',

    'question_text' : 'div.text-center:nth-child(2)',
    'answer_button_1' : 'button.w-full:nth-child(1)',
    'answer_button_2' : 'button.w-full:nth-child(2)',
    'answer_button_3' : 'button.w-full:nth-child(3)',
    'answer_button_4' : 'button.w-full:nth-child(4)',

    'game_score_text' : 'span.font-bold:nth-child(2)',

    'new_game_button' : 'a.px-7:nth-child(2)'
}

QUESTIONS_AND_ANSWERS = {
    'A cukorka ára negyedével, a csokoládé ára pedig ötödével csökkent úgy, hogy az árleszállítás után az áruk egyenlő lett. Hány tallérba került a cukorka az árleszállítás előtt, ha a csokoládé új ára 12 tallér?' : 4,
    'András 9 métert, Dani 10 métert korcsolyázik másodpercenként. Egy versenyen Dani 90 méter előnyt ad Andrásnak. A rajttól számítva hány másodperc alatt éri utol Dani Andrást?' : 2,
    'Melyik szám a 3, 7, 11, 15, … sorozat 2024. tagja?' : 1,
    'Mennyi a számjegyek összege abban a legnagyobb háromjegyű számban, amelyben a számjegyek szorzata 10-nél kisebb?' : 4,
    'Hány olyan négyjegyű szám van, amelyben 5 a számjegyek összege?' : 3,
    'Hány olyan háromjegyű prímszám van, melyben a számjegyek szorzata 15?' : 1,
    'Hány olyan négyjegyű szám van, amelyben van ismétlődő számjegy (pl. 2212, 4142, 1100)?' : 3,
    'Tíz egymást követő egész szám összege 123455. Mennyi az ezeket közvetlenül követő tíz szám összege?' : 4,
    'Mennyi a számjegyek összege abban a legkisebb háromjegyű pozitív egész számban, amelyben a számjegyek szorzata legalább 100?' : 2,
}



#################################################################################################



def print_by_letter(string:str, delay:float=0.1, end='\n') :
    for l in range(len(string)-1):
        sys.stdout.write(string[l])
        sys.stdout.flush()
        wait_seconds(delay*(random.random()+0.5) * (1 if string[l+1] != string[l] else 3 ))
    sys.stdout.write(string[-1])
    sys.stdout.flush()
    if end=='\n':
        print()
    else:
        print('',end=end)


def secs_to_text(seconds:float) :
    seconds = int(seconds)
    text = ""
    for i in range(len(TIME_CONVERT_LIST)):
        conv = TIME_CONVERT_LIST[i]
        if conv <= seconds:
            un = seconds//conv
            seconds -= un*conv
            text += str(un) + TIME_CHAR_LIST[i] + " "
    text = f'{text}\b'
    return text


def text_to_secs(text:str) :
    ls = text.split()
    secs = 0
    for v in ls:
        try:
            secs += TIME_CONVERT_LIST[TIME_CHAR_LIST.index(v[-1])]*int("".join(v[:-1]))
        except:
            return False
    return secs


def print_count_down_in_string(string:str, start:int, end=1, marker='[countdown here]'):
    print('',end="")
    previous_string_with_number_len = 0
    
    for i in range(start,end-2,-1):
        string_with_number = f'{i}'.join(string.split(marker))
        string_with_number_len = len(string_with_number)
        
        if string_with_number_len >= previous_string_with_number_len:
            print('\r'+string_with_number,end='')
        else:
            print('\r'+string_with_number+' '*( previous_string_with_number_len-string_with_number_len ),end='')

        if i != end-1:
            wait_seconds(1)
        
        previous_string_with_number_len = string_with_number_len
    
    print()


def xpath_by_outer_html(html):
    return f'//*[contains(., \'{html}\')]'




def get_element(css_selector_key='', outer_html_key='', xpath_key='', xpath=''):

    if css_selector_key != '':
        elements = driver.find_elements(By.CSS_SELECTOR, CSS_SELECTORS[css_selector_key])
    else:
        _xpath = ''
        if outer_html_key != '':
            _xpath = xpath_by_outer_html(OUTER_HTMLS[outer_html_key])
        elif xpath_key != '':
            _xpath = XPATHS[xpath_key]
        elif xpath != '':
            _xpath = xpath
        else:
            raise Exception("Function wait_for_element requires exactly one parameter. Please define either element css_selector_key, outer_html_key, xpath_key or xpath.")
            
        elements = driver.find_elements(By.XPATH, _xpath)
    
    if elements != []:
        return elements[0]
    else:
        return None


def wait_for_element(css_selector_key='', outer_html_key='', xpath_key='', xpath='',  timeout=60):
    
    if css_selector_key != '':
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTORS[css_selector_key])))
    else:
        _xpath = '' 
        if outer_html_key != '':
            _xpath = xpath_by_outer_html(OUTER_HTMLS[outer_html_key])
        elif xpath_key != '':
            _xpath = XPATHS[xpath_key]
        elif xpath != '':
            _xpath = xpath
        else:
            raise Exception("Function wait_for_element requires exactly one parameter. Please define either element css_selector_key, outer_html_key, xpath_key or xpath.")

        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, _xpath)))



def click_element_if_there(wait_seconds_between=0, css_selector_key='', outer_html_key='', xpath_key='',xpath='',  timeout=60):
    element = get_element(css_selector_key=css_selector_key, outer_html_key=outer_html_key, xpath_key=xpath_key, xpath=xpath)
    
    if 0 < wait_seconds_between :
        wait_seconds(wait_seconds_between)

    if element :
        element.click()

    return element


def wait_for_element_and_click(css_selector_key='', outer_html_key='', xpath_key='', xpath='',  timeout=60):
    element = wait_for_element(css_selector_key=css_selector_key, outer_html_key=outer_html_key, xpath_key=xpath_key, xpath=xpath,  timeout=timeout)
    element.click()

    return element
    




def get_goal_from_terminal():
    goal = input('Set goal _ ')
    goal_mode = ''

    if goal == '':

        goal_mode = 'run'
        goal = 0

    else:
        goal_in_seconds_if_time_goal = text_to_secs(goal)

        if goal_in_seconds_if_time_goal:
            goal_mode = 'time'
            goal = goal_in_seconds_if_time_goal
        
        else:
            goal_mode = 'cups'
            goal = int(goal)
        
    return goal_mode, goal

def get_mistake_rate_from_terminal(default_input:int):
    mistake_rate = input(f'mistake rate [{default_input}] : ')
    mistake_rate = int(mistake_rate) if mistake_rate != '' and mistake_rate != '\n' else default_input
    return mistake_rate

def get_difficult_from_terminal(default_input:str):
    difficulty = input(f'difficulty [{default_input}] : ')
    difficulty = difficulty if difficulty != '' and difficulty != '\n' else default_input
    return difficulty

def get_account_from_terminal(default_input:str):
    account = input(f'account a/j [{default_input}] : ')
    account = account if account != '' and account != '\n' else default_input
    return account


def initalize_browser_driver():

    driver_options = webdriver.FirefoxOptions()
    driver_options.headless = True

    driver = webdriver.Firefox(options=driver_options)

    driver.get("https://games.alphacademy.hu/")

    #driver.maximize_window()

    return driver


def log_into_website(username, password):
    driver.get("https://games.alphacademy.hu/login")

    username_input_field = get_element(css_selector_key='username_input_field')
    if username_input_field :
        username_input_field.send_keys(username)
    
    password_input_field = get_element(css_selector_key='password_input_field')
    if password_input_field :
        password_input_field.send_keys(password)

    click_element_if_there(css_selector_key='remember_me_checkbox')

    click_element_if_there(css_selector_key='login_button')


def get_score():
    return int(wait_for_element(css_selector_key='score_text').text)


def start_game():
    wait_for_element_and_click(css_selector_key=f'{difficulty}_difficulty_button')
    wait_for_element_and_click(css_selector_key='start_game_button')

def get_question_text():
    element = wait_for_element(css_selector_key='question_text')
    return element.text

def select_answer_for_question(question_text):
    answer_number = QUESTIONS_AND_ANSWERS[question_text]

    place = answer_number
    if mistake_rate != 0:
        make_mistake = random.randint(1, mistake_rate) == 1
        if make_mistake:
            place_options = [1,2,3,4]
            del(place_options[answer_number-1])
            place = place_options[ random.randint(0,2) ]
    
    wait_for_element_and_click(css_selector_key=f'answer_button_{place}')


def get_game_score():
    return int( wait_for_element(css_selector_key='game_score_text').text.split(' ')[0] )


def print_status():
    global _sum, score

    if goal_mode == "cups" :
        ETA = int( (now() - start_time) * (goal/_sum - 1) ) if not _sum == 0 and _sum < goal else 0
        if ETA > 0:
            ETAs.append(ETA)
        ETA_text = secs_to_text(ETA)

        percentage = int(_sum/goal*1000)/10

        print( f"Sum = {_sum}" + " "*(8-len(str(_sum))) + f"ETA: {ETA_text}" + " "*(18-len(ETA_text)) + f"{percentage}%" )

    elif goal_mode == "time" :
        percentage = int( (now() - start_time)/time_goal*1000 )/10

        passed_secs = now() - start_time
        rate = _sum / passed_secs
        expected_sum = rate * time_goal
        remaining_secs = time_goal - now() + start_time

        remaining_text = secs_to_text(remaining_secs)
        print( f"Sum = {_sum}" + " "*(8-len(str(_sum))) + f"rem: {remaining_text}" + " "*(18-len(remaining_text)) + f"expSum: {int(round(expected_sum,0))}" )

    elif "run" :
        elapsed_text = secs_to_text(now()-start_time)
        print( f"Sum = {_sum}" + " "*(8-len(str(_sum))) + f"elapsed: {elapsed_text}" + " "*(18-len(elapsed_text)) + f"Score: {score}")
        print()


def press_new_game():
    wait_for_element_and_click('new_game_button')





def play_a_game():
    global _sum, score, game_number
    
    start_game();   #print(f'\n{game_number}:',end='');   sys.stdout.flush()
    answered_count = 0

    question_text = ''
    previous_question_text = ''
    while answered_count < 6:
        while question_text == previous_question_text :
            question_text = get_question_text()

        select_answer_for_question(question_text)

        answered_count += 1

        previous_question_text = question_text
    
    game_score = get_game_score();   #print(" "*(7-len(str(game_number)))+(f"|| {game_score}" if game_score < 0 else f"|| +{game_score}"));   sys.stdout.flush()
    _sum += game_score

    game_number += 1

    score = get_score()

    #print_status()

    press_new_game()





# Example usage
if __name__ == "__main__":
    os.system('cls')
    if 1 == True :  # Fast mode 
        print()
        print_by_letter('### AlphaGames Bot 𝓌𝒾𝓉𝒽 𝓈𝑒𝓁𝑒𝓃𝒾𝓊𝓂  ###',0.08)
        print()
        print()


        goal_mode, goal = get_goal_from_terminal()

        mistake_rate = get_mistake_rate_from_terminal(default_input=21)

        account = get_account_from_terminal(default_input='j')
        username = ADAM_USERNAME if account == 'a' else JIMMY_USERNAME
        password = ADAM_PASSWORD if account == 'a' else JIMMY_PASSWORD

        difficulty = 'medium'


        print()
        print("> Initiating browser...")
    else:
        goal_mode, goal = 'run', 0
        mistake_rate = 21
        account = 'j'
        username = ADAM_USERNAME if account == 'a' else JIMMY_USERNAME
        password = ADAM_PASSWORD if account == 'a' else JIMMY_PASSWORD
        difficulty = 'medium'

    driver = initalize_browser_driver()

    print_count_down_in_string("- browser initiated, starting in: [countdown here].", 3)
    
    print()
    print("> Logging in", end=''); print_by_letter('...')

    while not get_element(css_selector_key='logout_button'):
        log_into_website(username=username, password=password)
        wait_seconds(2)
    print('- logged in.')
    
    element = wait_for_element_and_click(css_selector_key='games_section_button')

    starting_score = get_score()

    print()
    print()
    print(f'Score starting at:  {starting_score}')
    print_by_letter('Playing game...')

    start_time = now()
    _sum = 0
    game_number = 1
    score = start_game
    ETAs = []

    while goal_mode == 'run' or (goal_mode == "cups" and _sum < goal) or (goal_mode == "time" and (now() - start_time) < goal):
        play_a_game()


    driver.quit()
