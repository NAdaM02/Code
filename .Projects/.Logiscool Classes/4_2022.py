import random
#print(f'{a}{b}{c}')
#print(0b1111011) # bináris
#print(0x123AF) # hexadecimális
#print(0o164) # oktális

try:
    a = random.randint(-10, 10)
    b = random.randint(-10, 10)
    print(a/b)
except ZeroDivisionError:
    print('Cannot divide by zero.')
except:
    print('An unknown error occured.')
