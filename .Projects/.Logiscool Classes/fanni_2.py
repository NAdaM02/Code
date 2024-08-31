#my_name = "Fanni"
#my_age = 20

#print("Szia! A nevem " + my_name + "a korom pedig " + str(my_age))
#print("Szia! A nevem %s a korom pedig %s" %(my_name,my_age))

#gy = input("Mondj egy gyümölcsöt: ")
#he = input("Mondj egy helyet: ")
#es = input("Mondj egy eszközt: ")
#el = input("Mondj egy élőlényt: ")
#cs = input("Mondj egy cselekvést: ")

#print("Mikor %s-tm a(z) %s-n láttam egy %s-t, ahogy az egy %s-t evett egy %s-vl." %(cs,he,el,gy,es))

#nagykoru = True
#piros = False
#szep = input("Szép-e? (igen/nem) ").lower()

#if piros:
#    print("ez piros")
#else:
#    print("ez nem piros")

#if szep == "igen":
    #print("Ő szép")
    #szep = True
#else:
    #print("csunya")

#kor = int(input("Hány éves vagy? "))

#if kor < 18:
#    print("diák jegy")
#elif kor < 60:
#    print("felnőtt jegy")
#else:
#    print("nyugdíjas jegy")

nev1 = str(input("1. diák neve: "))
szazalek1 = int(input("Hány százalékos lett a dolgozata? "))
eredmeny1 = 0

nev2 = str(input("\n2. diák neve: "))
szazalek2 = int(input("Hány százalékos lett a dolgozata? "))
eredmeny2 = 0

if szazalek1 >= 90:
    eredmeny1 = "5-ös"
elif szazalek1 >= 80:
    eredmeny1 = "4-es"
elif szazalek1 >= 70:
    eredmeny1 = "3-as"
elif szazalek1 >= 50:
    eredmeny1 = "2-es"
else:
    eredmeny1 = "1-es"

if szazalek2 >= 90:
    eredmeny2 = "5-ös"
elif szazalek2 >= 80:
    eredmeny2 = "4-es"
elif szazalek2 >= 70:
    eredmeny2 = "3-as"
elif szazalek2 >= 50:
    eredmeny2 = "2-es"
else:
    eredmeny2 = "1-es"

print("\n%s dolgozata %s lett" %(nev1,eredmeny1))
print("%s dolgozata %s lett" %(nev2,eredmeny2))
