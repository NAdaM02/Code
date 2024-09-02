"""random = input()
ut = input()
hely = 0
for i in ut:
    if (i == 'L'):
        hely -= 1
    elif (i == 'R'):
        hely += 1
print(abs(hely))"""

En = []
Hano = []
kozos = 0

T = int(input())

N = int(input())
for i in range(N):
    A,B = input().split(' ')
    En.append([int(A),int(B)])

M = int(input())
for j in range(M):
    X,Y = input().split(' ')
    Hano.append([int(X),int(Y)])


h = 0
k = 0
for i in range(N):
    print('En: ', En)
    print('Hano: ', Hano)
    for j in range(M):

        if(j-h >= 0):
            if (En[i-k][1] >= Hano[j-h][1]):
                del Hano[j-h]
                h += 1
            else:
                break

    h_count = 0
    try:
        if (Hano[0][1] <= En[0][1]):
            kozos += Hano[0][1] - Hano[0][0]
            print(1)
            for j in range(1,M - h):
                if (Hano[j][0] - Hano[j-1][1] <= T and Hano[j][0] <= En[0][1]):
                    if(Hano[j][1] >= En[0][1]):
                        kozos += En[0][1]-Hano[j][0]
                        print(2)
                    elif(Hano[j][1] < En[0][1]):
                        kozos += Hano[j][1]-Hano[j][0]
                        print(3)
                else:
                    break
        else:
            print(4)
            kozos += En[0][1]-En[0][0]
    except:
        break
    del En[i-k]
    k += 1
    print('En valtozott:', En, '\n')
    print('Hano valtozott:', Hano)

print(kozos)
