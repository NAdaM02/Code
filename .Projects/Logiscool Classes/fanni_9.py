"""myList = []
for i in range(5):
    myList.append(input())
for i in range(0,5):
    print(myList[i], end=" ")"""

"""a = 3
b = 4
c = 5
print(a,b,c, sep="*")"""

"""myList = []
num = int(input("Melyik számon alkalmazzam a collatz sejtést? "))
myList.append(num)
while num != 1:
    if num % 2 == 0:
        num = int(num/2)
    else:
        num = int(num*3+1)
    myList.append(num)
print(myList, end=" ")"""

"""lista = []
for i in range(1,100):
    lista.append(i)
for i in range(len(lista)):
    if ("3" in str(lista[i]) and lista[i] % 3 == 0):
        lista[i] = "bimbum"
    elif(lista[i] % 3 == 0):
        lista[i] = "bim"
    elif ("3" in str(lista[i])):
        lista[i] = "bum"
print(lista)"""

"""password = input("Your password: ")
car = ["&","-","_","!","#","?",".","/","="]
strength = []
if len(password) >= 5:
    strength.append("|")
for c in password:
    if (c.islower()):
        strength.append("|")
    if (c.isupper()):
        strength.append("|")
    if (c.isnumeric()):
        strength.append("|")
    if (c in car):
        strength.append("|")
print("[ ", end="")
for i in range(len(strength)):
    print(strength[i], end="")
print(" ]")"""

a=3
b=4
c=5

if (a+b>c and b+c>a and a+c>b):
    print("Triangle")
else:
    print("Not a triangle")
