"""cleans = [] #[[day,(intervall)],...]
N,K = input().split(' ')
N = int(N)
K = int(K)
cap = input().split(' ')
trash = [0]
def clean(cleanable,day):
    cleans.append((day))
    for i in range(len(cleanable)):
        pass
    print(cleanable)


for i in range(N):
    cap[i] = int(cap[i])
    trash.append(0)
for day in range(K):
    typ,amo = input().split(' ')
    typ,amo = int(typ),int(amo)
    for i in range(N):
        if(trash[i]+amo > cap[i]):
            clean(i,day-1)
    trash[typ] += amo"""
