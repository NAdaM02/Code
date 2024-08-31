"""dict = {'cat' : 'Katze', 'dog' : 'Hund', 'horse' : 'Pferd'}
#empty_dict = dict()

print(dict)
#print(empty_dict)

print(dict['cat'])

words = ['cat', 'lion', 'horse']

for word in words:
    if word in dict:
        print(dict[word], end="  ")
    else:
        print("[ E r r o r : No such keyword. ]", end="  ")

for i in sorted(dict.keys()):
    print(dict[i])

for word in dict:
    print(word)

for german in dict.values():
    print(german)

for english, german in dict.items():
    print(english, '->', german)

dict['cat'] = 'Kätzchen'
dict['swan'] = 'Schwan'
dict.update({'duck' : 'Ente'})
print(dict)

del dict['dog']
dict.popitem()
print(dict)

uwu = {'gyanus' : 'sus', 'zalan' : '69', 'malac' : 'delicious', 'orban' : '1G'}
print(uwu)
uwu.update({'rossz': 'fortnite'})
print(uwu)
uwu['zalan'] = '09'
print(uwu)

dict1 = {1: 10, 2: 20}
dict2 = {3: 30, 4: 40}
dict3 = {5: 50, 6: 60}
dict4 = {}
for d in (dict1,dict2,dict3):
    dict4.update(d)
print(dict4)"""

students = {}
while(True):
    name = input("Student's name: ")
    if(name == ""):
        break
    score = int(input("Student's grades: "))
    if(name in students):
        students[name] += (score,)
    else:
        students[name] = (score,)

for name in sorted(students.keys()):
    sum = 0
    counter = 0
    for score in students[name]:
        sum += score
        counter += 1
    print(name, ":", sum/counter)
