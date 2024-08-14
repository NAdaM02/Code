def Sqrt(x,depth=53):
    if(x < 0):
        return 'Not applicable.'
    found = False
    r = 0
    while not found:
        if r**2 <= x and x < (r+1)**2:
            found = True
        else:
            r += 1
    if r**2 == x:
        return r
    ans = r+1/2
    if (ans)**2 == x:
        return ans
    for n in range(1,depth+1):
        if (abs(x-(ans - 1 / (2 ** n))**2) == abs(x-(ans + 1 / (2 ** n))**2)):
            ans = ans - 1 / (2 ** n)
            break
        if (abs(x-(ans - 1 / (2 ** n))**2) < abs(x-(ans + 1 / (2 ** n))**2)):
            ans = ans - 1 / (2 ** n)
        if (abs(x-(ans - 1 / (2 ** n))**2) > abs(x-(ans + 1 / (2 ** n))**2)):
            ans = ans + 1 / (2 ** n)
    return ans

x = float(input('sqrt '))
depth = input('depth ~53: ')
print()
if depth == '': print(Sqrt(x))
else: print(Sqrt(x,int(depth)))

"""x = int(input('x: '))
for i in range(100):
    x = Sqrt(x)
    print(x)
print(x)"""
