# 1. F e l a d a t   - 100 pont
"""N,P = input().split(' ')
N,P = int(N),int(P)
scores = []
Si1, Si2, Si3 = input().split(' ')
Davide = int(Si1)+int(Si2)+int(Si3)
for i in range(N-1):
    Si1, Si2, Si3 = input().split(' ')
    scores.append(int(Si1)+int(Si2)+int(Si3))
scores = sorted(scores, reverse=True)
if(scores[0]+P*100-Davide+1 > 0):
    print(scores[0]+P*100-Davide+1)
else:
    print(0)"""




# 2. F e l a d a t   - 100 pont
"""import math
N = int(input())
D = int(input())
A = 0
B = 0
for A in range(10**(N-1) + D - 10**(N-1) % D, 10**(N)-1, D):
    for B in range(10**(N-1) + D - 10**(N-1) % D, 10**(N)-1, D):
        if(math.gcd(A,B) == D and not(A == B)):
            print(A,B)
            exit()
print(0,0)"""




# 2. F e l a d a t   - 00 pont
N,Q = input().split(' ')
N,Q = int(N),int(Q)
order = input().split(' ')
taken_over = {}
for i in range(1,N+1):
    taken_over.update({str(i) : 0})
for j in range(Q):
    f = input()
    i = order.index(f)
    taken_over[str(order[i-1])] += 1
    print(sorted(taken_over.items(), key=lambda x: x[1], reverse=True)[0][0])
    order.pop(i)
    order.insert(i-1,str(f))
print(sorted(taken_over.items(), key=lambda x: x[1], reverse=True[0][0]))
