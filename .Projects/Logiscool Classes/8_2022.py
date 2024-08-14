wlist = ['cica', 'kutya', 'dínó', 'husky', 'ló', 'kádszéle', 'vitorlás']
dictionary = {}

for e in wlist:
    dictionary[e] = len(e)
print(dictionary)

def LongestWord(dictionary):
    k = list(dictionary.keys())
    v = list(dictionary.values())
    bigItem = k[0]
    bigIndex = 0
    for i in range(len(v)):
        if(len(k[i]) > len(bigItem)):
            bigItem = k[i]
            bigIndex = i
    print("\nDefinition 'LongestWord' has run. Here are the results: ")
    print(f"Longest word is '{k[bigIndex]}'")
#LongestWord(dictionary)

matrix = [[1,2],[3,4,5],[5,6,7,8]]
def MakeFullMatrix(matrix):
    n = len(max(matrix))
    for t in matrix:
        for i in range(n-len(t), 0, -1):
            t.append(0)
    print(matrix)
#MakeFullMatrix(matrix)

search = int(input('What number should we search for? '))
row = 1
column = 1
for i in matrix:
    for j in i:
        if j == search:
            print(f'The coordinates are: {row} {column}')
    row += 1
column += 1
row = 1
