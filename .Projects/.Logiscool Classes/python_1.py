#kúp térfogata
alap = int(input(Alap ))
mag = int(input(Magasság ))
print(Térfogat  + str(alap  mag  3))


#csere
v1 = alma
v2 = korte
seged = v1
v1 = v2
v2=seged


#prt és ps
lista=[1,2,3,4,5,6,7,12,31,5,314,2]
prt=[]
ps=[]
for e in lista
  if e % 2 == 0
    ps.append(e)
  else
    prt.append(e)
print(Páratlanok  + str(prt))
print(Párosok  + str(ps))


#legnépszerűbb gyümölcs
gyümölcs = [banán, papaya, alma, paradicsom]
pontok = [70,5,85,77]
maxi = 0
for i in range(len(pontok))
  if pontok[i]  pontok[maxi]
    maxi = i
print(gyümölcs[maxi])

maxi = pontok.index(max(pontok))
print(gyümölcs[maxi])


#minden szám osztható 7-tel, mondom...
lista = [1,2,3,4,5,6,7,89,3,6,7]
össz = 0
for i in range(len(lista)
  while (lista[i] % 7 != 0)
    lista[i] += 1
    össz += 1
print(Lista  + str(lista) +    Összes  + str(össz))


#magánhangzók
mondat="A cicák nagyon aranyosak, bárcsak lenne nekem is!"
maganh=['a','á','e','é','i','í','u','ú','ü','ű','o','ó','ö','ő']
össz = 0
for e in mondat
  if e in maganh
    össz += 1
print(valt)


#1-től x-ig
ig = int(input(Meddig ))
er = 0
for i in range(ig+1)
  er += i
print(er)


#számözön
puzzle = 1234
feher=0
fekete=0
piros=0
rounds = 0
while(fekete != 4)
  tipp = input(Tipp )
  feher=0
  fekete=0
  piros=0
  for i in range(4)
    if(tipp[i] in puzzle)
      if(tipp[i] == puzzle[i])
        fekete+=1
      else
        feher+=1
    else
      piros+=1
  print(Fekete + str(fekete))
  print(Fehér + str(feher))
  print(Piros + str(piros))
  rounds+=1
  print(This was your  + str(rounds) + . try. )
print(You won in  + str(rounds) +  rounds.)
print((The puzzle was  + puzzle + ))
