abc = "abcdefghijklmnopqrstuvwxyz"
A = str(input())
B = str(input())

lA = len(A)
lB = len(B)

rep = min(lA, lB)

if A+"a" == B:
    print(-1)
else:
    go_on = True
    for i in range(rep):
        if A[i] != B[i]:
            na = ord(A[i])-97
            nb = ord(B[i])-97
            if nb == na+1:
                if i == lB-1:
                    print(A[i], end="")
                else:
                    print(B[i], end="")
                    go_on = False
                    break
            else:
                print(abc[nb-1], end="")
                go_on = False
                break
        else:
            print(A[i], end="")

    if go_on:
        if lA == lB:
            print("z", end="")
        elif lA > lB:
            allz=True
            for i in range(rep, lA):
                print("z", end="")
                if A[i] != "z":
                    allz = False
                    break
            if allz:
                print("z", end="")
        else:
            print("a", end="")
