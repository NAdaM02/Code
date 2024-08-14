num_of_rods = int(input())
rods = list(map(int, input().split()))

rods.sort(reverse=True)

picks = []
count = 0
while count + 1 < num_of_rods :
    if (len(picks) < 4):
        if(rods[count] == rods[count+1]):
            picks.append(rods[count])
            picks.append(rods[count+1])
            count += 1
    else :
        count += num_of_rods
    count += 1

if len(picks) < 4 :
    print(0)
else :
    print(picks[0] * picks[2])
