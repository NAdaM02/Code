#szam = 1
#print(szam)
#szam += 7
#print(szam)
#szam -= 3
#print(szam)
#szam /= 4
#print(szam)
#szam **= 5
#print(szam)
#szam %= 6
#print(szam)
#szam //= 40
#print(szam)

#email = input("Adományozz email-címet (eskü nem adjuk el reklámozó oldalaknak)\n")
#if "@" in email and email.endswith(".com") or email.endswith(".hu"):
#    print("You'r such a failoure.")
#else:
#    print("Csak azért me' cigány vagyok?!")

#szam1 = int(input("1. szám: "))
#szam2 = int(input("2. szám: "))
#szam3 = int(input("3. szám: "))

#if (szam1 > szam2) and (szam1 > szam3):
#    print("Legnagyobb: " + str(szam1))
#elif (szam2 > szam1) and (szam2 > szam3):
#    print("Legnagyobb: " + str(szam2))
#else:
#    print("Legnagyobb: " + str(szam3))

#name = input("Név: ")
#allh = int(input("Összes óraszám: "))
#himh = int(input("Megjelent óraszám: "))

#if (allh/3*4) >= himh:
#    input("You'r still a failoure. (" + name + " részt vehet a vizsgán)")
#else:
#    input("Not good. (" + name + " nem vehet rész a vizsgán)")

#for i in range(1,10):
#    print(i)

#vmi = input("Valami: ")

#if vmi.endswith("cica") or vmi.endswith("kutya") or (vmi.endswith("delfin") and not("kacsa" in vmi)):
#    print("Jó")
#else:
#    print("Rossz")

for i in range(1,11):
    print(i**2)
