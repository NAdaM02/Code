gameOn = True
items = []
lives = 3
valasz = ""
room = 0
rooms = []
elso1 = 0
elso7 = 0

print("Egy ajtó pecsapódására ébredsz a földön. Mikor felülsz észre veszed, hogy valamitől nagyon fáj a fejed. Nagy nehezen felállsz és körülnézel. Tíz megszámozott ajtó húzódik végig a folyosón amin vagy, melyek mindegyike egy szobába vezet.")

while(gameOn and not lives <= 0):
  print("\nTárgyaid: " + str(items))
  print("Eddig ezekben a szobákban jártál: " + str(rooms))
  room = input("Melyik szobába mész be? ")
  if(room == "1"):
    if("1" not in rooms):
      rooms.append("1")
    if("lámpás" in items and "gyufa" in items and "olaj" in items):
      if (elso1 == 0):
        elso1 = 69
        print("Beleöntöd az olajat a lámpásba, előveszed a gyufát és meggyújtod. Így már nem félsz bemenni a szobába.")
      valasz = input("Belépsz az egyes szobába. Egy ajtót látsz rajta egy szöveges belépőkóddal. \nSzeretnéd megtippelni a jelszót?(igen/nem) ")
      if(valasz == "igen"):
        valasz = input("Mit tippelsz meg? ")
        if(valasz == "A kocka el van vetve" or valasz == "A kocka el van vetve." or valasz == "a kocka el van vetve" or valasz == "a kocka el van vetve."):
          print("Ügyes vagy, kijutottál! Mostmár végre vége van a rémálomnak. \n\n\n\n...legalábbis egyelőre.")
          gameOn = False
        else:
          lives -= 1
          print("Mikor megnyomod az OK-gombot az megráz téged. Rossz kódot adhattál meg, vesztettél egy életet. Ennyi életed maradt: " + str(lives))
    else:
      print("Beléptél az egyes szobába. Csak kis fény van, bemenni emiatt nem mersz bemenni. Talán valami majd segíthet.")

  if(room == "2"):
    if("2" not in rooms):
      rooms.append("2")
    if("feszítővas" not in items):
      print("Bemész a kettes szobába. Itt találsz egy feszítővasat. Ez valamire jó lehet.")
      items.append("feszítővas")
    else:
      print("Itt találtad a feszítővasat. Ez a szoba már nem rejt többet magában.")

  if(room == "3"):
    if("3" not in rooms):
      rooms.append("3")
    print("")

  if(room == "4"):
    if("4" not in rooms):
      rooms.append("4")
    print("")

  if(room == "5"):
    if("5" not in rooms):
      rooms.append("5")
    print("")

  if(room == "6"):
    if("6" not in rooms):
      rooms.append("6")
    print("")

  if(room == "7"):
    if("7" not in rooms):
      rooms.append("7")
    if(elso7 == 0):
      elso7 += 1
      valasz = input("Bemész a hetes szobába. Körülnézel és meglátsz egy ládát a szoba közepében lévő asztalon. Ám akárhogy keresed, nem találsz semmilyen hozzákapcsolódó kombinációs zárat. Megpróbálod szétfeszíteni a kezeddel de az nem működik. Tárgyaid: " + str(items) + " \nMegpróbálod valahogy máshogy kinyitni?(igen/nem) ")
      if(valasz == "igen"):
        if("feszítővas" in items):
          print("Előveszed a feszítővasad és nagy nehezen kinyitod a ládát benne rejlik egy üveg olaj. Ez később jól jöhet valamire.")
          items.append("olaj")
        else:
          lives -= 1
          print("Mivel nincs más amivel ki tudnád nyitni elkezded a fogaddal feszegtni ami kitörik. Vesztesz egy életet. Ennyi életed maradt: " + str(lives))
    

  if(room == "8"):
    if("8" not in rooms):
      rooms.append("8")
    print("")

  if(room == "9"):
    if("9" not in rooms):
      rooms.append("9")
    print("")

  if(room == "10"):
    if("10" not in rooms):
      rooms.append("10")
    print("")


