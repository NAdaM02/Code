nevek = ["1Alma", "2Alma", "3Alma", "4Alma", "5Alma", "6Alma", "7Alma", "8Alma", "9Alma", "10Alma"]
"""
#lista = [1,2,3]
#Alma = "Alma1"
#nevek = [Alma, "Peti", "Gergő"]
#print(nevek)
#print(len(nevek))

nevek = ["Alma", "Én"]
számok = ["73", "21", "37", "12", "1001001"]
állatok = ["Cica", "Hollóképű rókaholló", "Sivatagi lapátfülű denevér"]
valasz = input("Melyik lista hosszára vagy kíváncsi? [nevek|számok|állatok]: ")

if valasz == "nevek":
    print(len(nevek))
if valasz == "számok":
    print(len(számok))
if valasz == "állatok":
    print(len(állatok))
"""
"""
nevek = ["1Alma", "2Alma", "3Alma", "4Alma"]
#index = int(input("Hányas index? :"))
#print(nevek[index-1])

#print(nevek[len(nevek)-1])
#print(nevek[-1])

j = len(nevek)
print("Add meg az indexet!")
while j < len(nevek)*(-1) or j > len(nevek)-1:
    j = int(input("Index? "))
    if not(j < len(nevek)*(-1) or j > len(nevek)-1):
        print(nevek[j-1])
    else:
        print("An error has occured. [Error type: wrong index] (Error code: 125643n)")
"""
"""
i = 0
while i < len(nevek):
    print(nevek[i])
    i += 1

list = []
i = 1
while i <= 50:
    list.append(str(i) + "Alma")
    i += 1
print(list) """

""" i = 1
paros = []
paratlan = []
while i <= 20:
    if i % 2 == 0:
        paros.append(i)
    else:
        paratlan.append(i)
    i += 1
print(paratlan)
print(paros) """

"""szamok = [1,2,3,4,5]
szamok.insert(1,10)
print(szamok)
szamok.insert(11, 11)
print(szamok)
szamok.insert(10, 12)
print(szamok) """

""" i = 2 # szamok[i]
j = 4 # szamok[j]

seged = nevek[i+1]
nevek[i+1] = nevek[j+1]
nevek[j+1] = seged
print(nevek) """

""" szamok = [0,0,0,1,2,3,4,5,6,7]
print(szamok)
szamok.pop(2)
print(szamok)
szamok.remove(3)
print(szamok) """

""" szamok = [0,0,0,0,1,1,1,1,1,2,2,2,3,4,5,55,6,7,8,9,1000]
vizsg = int(input("Melyik számot akarod vizsgálni? "))
hany = 0
i = 0
while i < len(szamok):
    if szamok[i] == vizsg:
        hany += 1
    i += 1
print(hany) """

szamok = [0,0,0,0,1,1,1,1,1,2,2,2,3,4,5,55,6,7,8,9,1000]
össz = 0
i = 0
while i < len(szamok):
    össz += szamok[i];
    i += 1;
print(össz)
