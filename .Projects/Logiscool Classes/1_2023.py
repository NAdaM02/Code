def Feladat1():
    inp = input("Give me an input and I'll give you the first and last two characters of it.\n")
    if(len(inp) >= 2):
        print(inp[:2] + inp[-2:])

def Feladat2():
    inp = input('Give me an input:\n')
    inp = (inp.replace(str(inp[0]).lower(), '$')).replace(str(inp[0]).upper(), '$')
    print(inp)

def Feladat3():
    inp = input('Give me an input:\n')
    x = 4
    dic = {}
    for i in inp:
        dic.update({i:0})
    for i in inp:
        dic[i] = dic.__getitem__(i)+1
        if(dic.__getitem__(i) == x):
            print("'",i,"' is the character that occurs ",x," times first.", sep='')
            break

def Feladat4():
    my_matrix = [[1,2,3], [4,5,6], [7,8,9,10]]
    my_list = []
    for i in my_matrix:
        for j in i:
            my_list.append(j)
    print(my_list)

def Feladat5():
    x = int(input('Hányadik elemet töröljem? '))-1
    valt = ('a','b','c','d','e','f','g','h','i','j')
    valt = list(valt)
    del valt[x]
    valt = tuple(valt)
    print(valt)

def Feladat6():
    dic = {'Red':1, 'Green':2, 'Blue':3, 'Yellow':4}
    c = input("Do you want me to sort in descending or ascending order? ['d'/'a']\n")
    if (c == 'a'):
        res = False
    elif (c == 'd'):
        res = True
    else:
        return 0
    print(dict(sorted(dic.items(), key=lambda x: x[1], reverse=res)))

def Feladat7():
    """n = 3
    x = 10
    nums = []
    for i in range(1,x+1):
        nums.append(i)
    print(nums,'\n')
    while (len(nums) > n):
        b = len(nums)
        for i in range(0,b):
            if(i % n == 0 and i-1 < len(nums)):
                del nums[i-1]
        print(nums)"""


#Feladat1()
#Feladat2()
#Feladat3()
#Feladat4()
#Feladat5()
Feladat6()
#Feladat7()
