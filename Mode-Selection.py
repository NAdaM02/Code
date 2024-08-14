import keyboard

selected = False
mode_selected = "Mode:  >goal<  time "
def pressed_left(event) :
    global mode_selected
    if event.event_type == keyboard.KEY_DOWN:
        mode_selected = "Mode:  >goal<  time "

def pressed_right(event) :
    global mode_selected
    if event.event_type == keyboard.KEY_DOWN:
        mode_selected = "Mode:   goal  >time<"

def pressed_enter(event) :
    global selected
    if event.event_type == keyboard.KEY_DOWN:
        selected = True

def modeSelect() :
    global mode_selected
    global selected
    selected = False

    keyboard.on_press_key('left', pressed_left)
    keyboard.on_press_key('right', pressed_right)
    keyboard.on_press_key('enter', pressed_enter)

    while not selected:
        print('\r',mode_selected,sep="",end="")
    input()
    keyboard.unhook_key('left')
    keyboard.unhook_key('right')
    keyboard.unhook_key('enter')

    if mode_selected == "Mode:  >goal<  time ":
        return "goal"
    elif mode_selected == "Mode:   goal  >time<":
        return "time"

modeSelect()