# Adatstruktúrák
# string (str) - str()
# dictionary - dict()
# integer (int) - int()
# list (matrix)
# float
# bool
# tuple

# Változó nevek
# Kötelező: nem lehet szóköz, betűvel kell kezdődnie (kivéve _), case sensitive (számít a kis/nagybetű)
# Python kulcsszó nem lehet
# Konvenciók: snake_case
#
myInteger = 42
myString = "Logiscool"
myFloat = 3.14
myBool = True
myList = ["apple", "orange", "pear", "kiwi"]
myMatrix = [[4, 5, 3], [1, 9, 7], [8, 2, 6]]
myTuple = (55, 120, 200)
myDictionary = {"first": 1, "second": 2, "third": 3}

# #
# for i in myString:
#     print(i, end="")
# print("")
# for i in myList:
#     print(i, end=", ")
# print("")
# for row in myMatrix:
#     for item in row:
#         print(item)
# for i in myTuple:
#     print(i)
# for i, j in myDictionary.items()

# Mutable vs immutable
# mutable: list, dict
# immutable: tuple, int, float, string, bool
# print(myInteger)
# print("id: ", id(myInteger))
# myInteger = 100
# print(myInteger)
# print("id: ", id(myInteger))
# print("List id: ", id(myList))
# myList.append(4)
# print("List id: ", id(myList))
#
# myTupleList = ([1, 2, 3], 4, 5, 7)
# myTupleList[0]

# Típuskonverziók
# int -> float, string
# float -> string, int (!)
# string -> float, int, list (!), tuple (!)
# list -> string (!), tuple
# tuple -> list, string (!)

# try:
#     x = float(input("Enter a number:\n"))
#     y = -2*x**4 + 3*x**3 + 2*x**2 - 7*x + 4
#     print(y)
# except ValueError:
#     print("Can't convert to float")

# Oszthatóság: 1000-2500 közötti számok amik oszthatók 7-el, de 5-el nem
# list = []
# for i in range(1000, 2501):
#     if i % 7 == 0 and i % 5 != 0:
#         list.append(i)
# print(list)

# Pontos idő, eltelt másodpercek alapján
seconds = int(input())
if seconds >= 24*60*60:
    seconds = seconds % (24*60*60)
minutes = seconds // 60
seconds = seconds % 60
hours = minutes // 60
minutes = minutes % 60
print("The exact time is: ", hours, ":", minutes, ":", seconds)
