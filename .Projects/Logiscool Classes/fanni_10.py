"""for i in range(1,6):
    for j in range(i):
        print(i, end=" ")
    print("")"""


"""for i in range(1300,2000):
    if (i % 28 == 0):
        print(i, end=" ")
print("")"""


"""vnevek=["Szabó","Nagy","Kocsis"]
knevek=["Anna","Peti","Balázs"]

for vnev in vnevek:
    for knev in knevek:
        print(vnev,knev)"""


nevek=["Anna","Marci","Balázs","Tomi","Ádám","Dani","Peti","Fanni"]

for i in range(len(nevek)):
    for j in range(len(nevek)):
        if (i < j):
            print(nevek[i],nevek[j])


"""def sus(n):
    print(n)

sus(10)"""


"""def prime(n):
    prim = True
    for i in range(2,n):
        if(n % i == 0):
            prim = False
    print(str(prim) + " " + str(n))
prime(67)"""

