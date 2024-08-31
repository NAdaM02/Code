def p(s):
    print(str(s))
def pn(s):
    print("\n" + str(s))
def ps(s, endw=" "):
    print(str(s), end=str(endw))
def num():
    return(int(input("Adj meg egy szamot: ")))
def inp():
    return(input("Adj meg egy valamit: "))

#1-tolValameddigASzamok
"""def plus(n):
    if (n >= 1):
        ps(n)
        return f1(n-1)
plus(num()) """


#2.faktorialis
"""def factor(n):
    if (n >= 1):
        return n * factor(n-1)
    else:
        return 1
p(factor(num()) """


#valahanyadikFibonacci
"""def fib(n):
    if (n == 1):
        return 1
    if (n==2):
        return 1
    else:
        return fib(n-1) + fib(n-2)
p(fib(num())) """


#szamolos
"""def count(n):
    if (n >= 1):
        return n + count(n-1)
    else:
        return 1
p(count(num())-1) """


#reciprokOsszeados
"""def reci(n):
    if (n >= 1):
        return 1/n + reci(n-1)
    else:
        return 1
p(reci(num())-1) """


#hatvany
"""def hatvany(a,b):
    if (b >= 1):
        return a * hatvany(a,b-1)
    else:
        return 1
p(hatvany(num(), num()) """


#ceaserTitkositas
"""mondat = []
def caesar(szoveg, kulcs):
    hossz = len(szoveg)
    kodol(szoveg,kulcs,hossz)

def kodol(szoveg,kulcs,hossz,count=0):
    if (count < hossz):
        #ord()  betu => szam
        #chr()  szam => betu
        ujindex = (ord(szoveg[0]) + kulcs) % 122
        if ujindex == 0:
            mondat.append(chr(122))
        elif ujindex < 97:
            mondat.append(chr(ujindex + 96))
        else:
            mondat.append(chr(ujindex))
        kodol(szoveg[1:], kulcs, hossz, count+1)
    else:
        temp = ""
        ujszo = temp.join(mondat)
        print(ujszo)
caesar("alma finom",3) """


#egylesz
def egylesz(sz):
    if (sz > 1):
        ps(int(sz), endw=" -> ")
        if (sz % 2 == 0):
            egylesz(sz/2)
        else:
            egylesz(sz*3+1)
    else:
        p(int(sz))
        return 1
egylesz(num())
