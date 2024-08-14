workdays, orders = input('').split()
workdays = int(workdays)
orders = int(orders)
dues = [[],[]]

def IncreasingOrder(list):
    increasing_order = [[],[]]
    while(len(list[0]) > 0):
        smallest = 0
        for i in range(len(list[0])):
            if(list[0][i] < list[0][smallest]):
                smallest = i
        increasing_order[0].append(list[0][smallest])
        increasing_order[1].append(list[1][smallest])
        del list[0][smallest],list[1][smallest]
    return increasing_order

for i in range(orders):
    dues[0].append(int(input()))
    dues[1].append(i+1)
dues = IncreasingOrder(dues)
works = []

if(workdays < orders):
    repeat = workdays+1
else:
    repeat = orders

for i in range(1,repeat):
    if(len(dues) < 1):
        break
    for j in range(len(dues)-1):
        if(dues[0][j] < i):
            del dues[0][j],dues[1][j]
    if(i <= dues[0][0]):
        works.append([dues[1][0],i])
        del dues[0][0], dues[1][0]

print(len(works))
for work in works:
    print(f'{work[0]} {work[1]}')
