"""for i in range(10):
    print(i)
for i in range(1,11):
    print(i)
for i in range(1,20,2):
    print(i)
for i in range(0,21,2):
    print(i)
for i in range(0,101,3):
    print(i)

sz="Szia! Hogy vagy?"

for c in sz:
    print(c) """

"""mivel = int(input("Mivel? "))
meddig = int(input("Meddig? ")) + 1

for i in range(1,meddig):
    print(str(mivel) + " * " + str(i) + " = " + str(mivel*i))"""

"""sz = "an caircaánky onsaagkyo"
sz1 = ""
sz2 = ""
for i in range(0, len(sz), 2):
    sz1 += sz[i]
for i in range(1, len(sz), 2):
    sz2 += sz[i]
eredmeny = sz1 + sz2
print(eredmeny)

sz = "a cicák nagyon aranyosak"
eredmeny = ""
fel = len(sz)+1 // 2
sz1 = sz[:fel]
sz2 = sz[fel:]
for i in range(fel):
    eredmeny += sz1[i]
    if i < len(sz2):
        eredmeny += sz2[i]
print(eredmeny)"""

lista = []
for i in range(9,-27,-1):
    lista.append(i)
print(lista)
