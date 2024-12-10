import sys

T = int(input())

for test in range(1, T+1):
    N, K = map(int, input().split())
    ans = False

    if K==1:
        ans = True
    elif N==2:
        ans = False
    elif int(K*(K+1)/2) == N or int(K*(K+1)/2) == N-1:
        ans = True

    if ans == True:
        print("YES")
    else:
        print("NO")

sys.stdout.close()
