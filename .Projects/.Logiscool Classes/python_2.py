"""gameOn = True
life = 3
items = []
rooms = []
code = "5397"

while (gameOn and life > 0):
  room = int(input("Melyik szobába mész?\n"))
  if(room == 1):
    if("kulcs" not in items):
      print("Kulcs.")
      items.append("kulcs")
      if("doboz" in items):
        print("Van már egy ládád és egy kulcsod is, így kinyitod.\nTalálsz benne egy cetli, rajta az 1234 számokkal.")
    else:
      print("𝘒𝘶𝘭𝘤𝘴 𝘮ú𝘭𝘵 𝘪𝘥ő𝘣𝘦𝘯")
  if(room == 2):
    if("doboz" not in items):
      items.append("doboz")
      if("kulcs" in items):
        print("Van már egy ládád és egy kulcsod is, így kinyitod.\nTalálsz benne egy cetli, rajta az 1234 számokkal.")
  if(room == 3):
    print("Ajtó kóddal.")
    valasz = input("Kinyitod?(igen/nem)\n")
    if valasz == "igen":
      tipp = input("Tipp: ")
      if(tipp == code):
        print("kijutottál")
        gameOn = False
      else:
        life -= 1"""


"""print("Belépsz a Nasa űrállomásra.")
valasz = int(input("Válassz...\n1 - Kinézel az ablakon\n2 - Amongsus in real life 100% danegrus!%%!!++\n3 - Átveszed a hajó irányítását\n"))
if(valasz == 1):
  print("Látsz egy űrcicát, bejengeded, meghalsz.")
if(valasz == 2):
  print("You were ejected...")
if(valasz == 3):
  print("Belerepülsz a cicák bolygójába.")"""
