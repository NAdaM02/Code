andi = tuple(map(int, input().split()))
bandi = tuple(map(int, input().split()))

tav = 0
for i in range(3):
    tav += abs(andi[i]-bandi[i])

print(tav)
