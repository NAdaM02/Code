import tkinter as tk
from PIL import ImageTk

inp = ''
modes = ['Stacks','Skulkers']
mode = 0
entered = False

def clicked_number(num):
    global inp, entered
    if entered:
        Clear()
        entered = False
    inp += str(num)
    text_out.delete(1.0, "end")
    text_out.insert(1.0, inp)
def Clear():
    global inp
    text_out.delete(1.0, "end")
    inp = ''
def Enter():
    global entered,inp
    while inp[0] == '0':
        inp = inp[1:]
    if not inp == '':
        blocks = int(eval(inp.replace('x','*')))  # user input
        size_of_stack = 64  # cycle between 64/16/1
        output = ''
        if mode == 1:
            stacks = int(blocks / size_of_stack)
            shulker_boxes = int(stacks / 27)
            stacks = stacks - shulker_boxes * 27
            blocks = blocks - shulker_boxes * 27 * size_of_stack - stacks * size_of_stack
            """print(f'{shulker_boxes} shulker boxes, {stacks} stacks, {blocks} blocks')"""
            if not shulker_boxes == 0:
                output += f'{shulker_boxes} shulker boxes \n'
            if not stacks == 0:
                output += f'{stacks} stacks \n'
            if not blocks == 0:
                output += f'{blocks} blocks \n'
        elif mode == 0:
            if not blocks < 64:
                output += f'{blocks // 64} stacks \n'
            if not blocks % 64 == 0:
                output += f'{blocks % 64} blocks \n'
        text_out.delete(1.0, 'end')
        text_out.insert(1.0, output)
        entered = True
def Mode():
    global mode,entered
    mode += 1
    mode = mode % len(modes)
    btn_mode = tk.Button(root, text=modes[mode], command=lambda: Mode(), width=6, font=('Arial', 14))
    btn_mode.grid(row=6, column=2)
    if entered:
        Enter()
def Multiply():
    global inp
    inp+='x'
    text_out.delete(1.0, "end")
    text_out.insert(1.0, inp)
def Addition():
    global inp
    inp += '+'
    text_out.delete(1.0, "end")
    text_out.insert(1.0, inp)

bg_colour = '#202020'

# initialize app
root = tk.Tk()
root.title('Minecraft Calculator')
root.eval('tk::PlaceWindow . center')
root.geometry('293x364')

# frame1
frame1 = tk.Frame(root, width=402, height=603, bg=bg_colour)
#frame1.grid(row=0,column=0)

# text
text_out = tk.Text(root, height=4, width=16, font=('Arial',24))
text_out.grid(columnspan=5)

# background
bg_img = ImageTk.PhotoImage(file='assets/calculator_style_input_gui.png')
bg_widget = tk.Label(frame1, image=bg_img)
bg_widget.image = bg_img
bg_widget.pack()

# button widgets
btn_1 = tk.Button(root, text='1', command=lambda:clicked_number(1), width=8, font=('Arial',14))
btn_1.grid(row=2,column=1)
btn_2 = tk.Button(root, text='2', command=lambda:clicked_number(2), width=8, font=('Arial',14))
btn_2.grid(row=2,column=2)
btn_3 = tk.Button(root, text='3', command=lambda:clicked_number(3), width=8, font=('Arial',14))
btn_3.grid(row=2,column=3)
btn_4 = tk.Button(root, text='4', command=lambda:clicked_number(4), width=8, font=('Arial',14))
btn_4.grid(row=3,column=1)
btn_5 = tk.Button(root, text='5', command=lambda:clicked_number(5), width=8, font=('Arial',14))
btn_5.grid(row=3,column=2)
btn_6 = tk.Button(root, text='6', command=lambda:clicked_number(6), width=8, font=('Arial',14))
btn_6.grid(row=3,column=3)
btn_7 = tk.Button(root, text='7', command=lambda:clicked_number(7), width=8, font=('Arial',14))
btn_7.grid(row=4,column=1)
btn_8 = tk.Button(root, text='8', command=lambda:clicked_number(8), width=8, font=('Arial',14))
btn_8.grid(row=4,column=2)
btn_9 = tk.Button(root, text='9', command=lambda:clicked_number(9), width=8, font=('Arial',14))
btn_9.grid(row=4,column=3)
btn_0 = tk.Button(root, text='0', command=lambda:clicked_number(0), width=8, font=('Arial',14))
btn_0.grid(row=5,column=2)

btn_enter = tk.Button(root, text='<-', command=lambda:Enter(), width=5, height=2, font=('Arial',14))
btn_enter.grid(row=6,column=3)

btn_clear = tk.Button(root, text='C', command=lambda:Clear(), width=5, height=2, font=('Arial',14))
btn_clear.grid(row=6,column=1)

btn_mode = tk.Button(root, text=modes[mode], command=lambda:Mode(), width=6, font=('Arial',14))
btn_mode.grid(row=6,column=2)

btn_multiply = tk.Button(root, text='x', command=lambda:Multiply(), width=3, font=('Arial',14))
btn_multiply.grid(row=5,column=1)

btn_add = tk.Button(root, text='+', command=lambda:Addition(), width=3, font=('Arial',14))
btn_add.grid(row=5,column=3)

# run app
root.mainloop()



#process

#process end
