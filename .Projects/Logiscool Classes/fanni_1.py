# print(input("Kő' kő?"))
# print(input("alma?").__len__())  # __len__ a szó hossza
# print("az alma piros".split(' '))
# print("xaxbxcaaxxhf".split('x'))  # elválasztás xy-al
# print("az alma nagyon piros".count('a'))  # xy megszámolása a szövegben
# print("bcdefaagl".find('a'))  # első xy betű helyét írja ki
# print("sadasdasd".startswith('s'))  # xy betűvel kezdődik-e
# isnumeric()  szám-e
# isalpha()  csak betu
# islower()  csak kicsi
# isupper()  csak nagybetu
# print(input("True- kiabálás, False- nem kiabalas\nmi a mondat? ").isupper())  # xy full nagybetű-e

# valtozo1=12  # adunk egy értéket
# print(valtozo1)  # kiírjuk 12
# valtozo1="alma"  # változtatjuk a valtozo értékét
# print(valtozo1)  # kiírjuk alma

# nev = "János"  # random változó
# kor = 23  # random változó
# hajszin = "barna"  # random változó
# tudProgramozni = True  # random változó
# foglalkozas = "tanár"  # random változó

# print("az élet nagyon szép".split(' ').__len__())  # megszámoljuk hány szó
# print("Cica egy cica, aki nagyon cica".lower().count('cica'))  # megszámoljuk hány cica------------------------------------

# szam1="10"
# szam2=20
# print("osszeg")
# szam3 = 3.5
# szam4 = "szia"
# print(szam4)
# print('a'+' '+'a')
# print(type(szam1))
# print(type(szam2))
# print(type(szam3))
# szam4 = int(szam1)
# print(szam4+2)

# "10 => 10 int()
#  10 => "10" str()

# nev = "Ádám"
# kor = 13
# print("Hajimemaste " + nev + " desu, " + str(kor) + " éves.")

# r = float(input("Mennyi a kör sugara? "))
# K = 2*3.14*r
# print("Kerület:" + str(K))

i = int(input("Első szám: "))
ii = int(input("Második szám: "))
iii = int(input("Harmadik szám: "))
iv = int(input("Negyedik szám: "))
v = int(input("Ötödik szám: "))

print(i+ii-iii*iv/v)
