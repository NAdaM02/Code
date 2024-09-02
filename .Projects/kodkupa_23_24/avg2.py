from math import ceil as felkerekitve
db, atlag = input().split()
db, atlag = int(db), int(atlag)
arak = list(map(int, input().split()))

cel = db*atlag
ossz_ar = sum(arak)
valtozas_atlag = (cel - ossz_ar) / db
valtozas = max(1,felkerekitve(abs(valtozas_atlag)) - 1)

"""print()
print("Sum:",ossz_ar)
print("Cel:",cel)
print()"""

ok = False
valt = 0
while not ok :
    uj_ossz = ossz_ar
    for ar in arak:
        elteres = cel - uj_ossz
        if abs(elteres) > valtozas :
            valt = valtozas * abs(elteres)/elteres
        else:
            valt = elteres
        uj_ossz += valt
        if (ar + valt) < 1 :
            #print("_",valt + 1 - ar - valt,"_", end="", sep="")
            uj_ossz += 1 - (ar + valt)
        #print(uj_ossz, end=" ")
    #print()
    if cel - uj_ossz == 0:
        ok = True
    else:
        valtozas += 1
print(valtozas)
#print()
