def p(param1 =""):
    print(str(param1))
def pn(param1 =""):
    print("\n" + str(param1))
def ps(param1 =""):
    print(str(param1), end=" ")


"""def isPrime(s):
    prime = True
    for i in range(2,s-1):
        if (s % i == 0):
            prime = False
    if(prime):
        print("Ez egy prím szám.")
    else:
        print("Ez egy összetett szám.")
isPrime(12) """

"""def is90(a,b,c):
    is90 = False
    if(a**2+b**2==c**2 or a**2+c**2==b**2 or b**2+c**2==a**2):
        is90 = True
    if(is90):
        pn("Ez egy derékszögű háromszög.")
    else:
        pn("Ez nem egy derékszögű háromszög.")
is90(3,4,6) """

"""def absolute(p):
    if p >= 0:
        return p
    else:
        return -p
pn(absolute(-69))
p(absolute(1)) """

"""def exit():
    for i in range(1,10):
        ps(i)
        if(i == 6):
            return 0
exit()"""

"""def veryBig(a,b,c):
    biggest = a
    if (biggest < b > c):
        biggest = b
    if (biggest < c > b):
        biggest = c
    pn(biggest)
veryBig(1,3,2)"""

"""def sumList(list1):
    sum = 0
    for i in range(len(list1)):
        sum += list1[i]
    print(sum)
sumList(list1 = [1,2,3])"""
