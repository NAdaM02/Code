import math

d = int(input('Diameter: '))

def GetCords(d):
    circle = [[], []]
    for i in range(1,360):
        if (i > 90 or i < 270):
            modifierx = 1.0
        elif (i > 90 or i < 270):
            modifierx = -1.0
        else:
            modifierx = 0
            modifiery = 0
        if (i > 180):
            modifiery = 1.0
        elif (i < 180):
            modifiery = -1.0
        else:
            modifierx = 0
            modifiery = 0
        circle[0].append(int(math.cos(i)*d*modifierx))
        circle[1].append(int(math.sin(i)*d*modifiery))
    return circle

def ShowCircle(circle):
    minx = min(circle[0])
    maxx = max(circle[0])
    miny = min(circle[1])
    maxy = max(circle[1])
    for y in range(miny-1,maxy+1):
        for x in range(minx-1,maxx+1):
            isPoint = False
            for k in range(len(circle[0])):
                if (x == circle[0][k] and y == circle[1][k] and not (circle[0][k] == 0 and circle[1][k] == 0)):
                    isPoint = True
            if (isPoint):
                print(' o ', end='')
            else:
                print('   ', end='')
        print('')
ShowCircle(GetCords(d))
