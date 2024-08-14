import math

"""num = int(input('Enter a number:\n'))
while (num > 1):
    if (num % 3 == 0):
        num /= 3
    else:
        num += 1
        print(num)
print(num)"""

"""cond = True
i = 0
while (cond):
    print(i)
    i += 1
    if (i >= 500000):
        cond = False"""

"""myList = ['dog', 'cat', 'lizard', 'hamster', 'guinea pig', 'parrot', 'cameleon']
i = 0
while (i < len(myList)):
    print(myList[i], end=' ')
    i += 1"""

"""basket = {'apple': 20, 'banana': 30, 'orange': 10}
fruit = input('Enter a fruit!\n')
for item in basket.keys():
    if (item == fruit):
        print('This fruit is already in the basket.')
        break
else:
    quantity = int(input('Enter quantity:\n'))
    basket[fruit] = quantity
    print(basket)"""

"""inp = input('Give me an input: ')
numbers = 0
letters = 0
for i in inp:
    try:
        n = int(i)
        numbers+=1
    except:
        if(i != ' '):
            letters += 1
print(f'Amount of letters: {letters}     Amount of numbers: {numbers}')"""

"""num = int(input('Give me a number:\n'))
def isPrime(n):
    prime = True
    for i in range(2,int(math.sqrt(n))):
        if(n % i == 0):
            prime = False
            break
    return prime
if (isPrime(num)):
    print('This is not a prime number.')
else:
    print('This is a prime number.')"""

"""num = int(input('Give me a number:\n'))
lista = []
def isPrime(n):
    prime = True
    for i in range(2,int(math.sqrt(n))+1):
        if(n % i == 0):
            prime = False
            break
    return prime
x = 2
while (x < num):
    if(isPrime(x) == True):
        print(x, end=' ')
        if(x != 2):
            x += 1
    x += 1
    lista.append(x)
print(lista)"""

rows = int(input("How many rows should the matrix have? "))
cols = int(input("How many columns should the matrix have? "))
matrix = []
seged = []
for i in range(cols):
    seged.append('0')
for i in range(rows):
    matrix.append(seged)
print(matrix)
for i in range(rows):
    for j in range(cols):
        print(matrix[i][j], end = '  ')
    print('')
