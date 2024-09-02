num_of_matches = int(input())
matches = []
for i in range(num_of_matches):
    matches.append(list(map(int, input().strip().split())))
for match_num in range(num_of_matches):
    c1,c2 = matches[match_num]
    if  c1 == 33 and c2 <= 30 :
        # 3 matches
        for i in range(3):
            if c2 > 10 :
                p2 = 10
            else:
                p2 = c2
            print(11, p2)
            c1 -= 11
            c2 -= p2
    elif  33 <= c1 <= 43 and 11 <= c2 <= 41 :
        # 4 matches
        print(c1-3*11, 11)
        c1 -= c1-3*11
        c2 -= 11
        for i in range(3):
            if c2 > 10 :
                p2 = 10
            else:
                p2 = c2
            print(11, p2)
            c1 -= 11
            c2 -= p2
    elif  33 <= c1 <= 53 and 22 <= c2 <= 52 :
        # 5 matches
        if  c1 - 3*11 > 10:
            print(10, 11)
            c1 -= 10
            c2 -= 11
        else:
            print(0, 11)
            c2-=11
        print(c1-3*11, 11)
        c1 -= c1-3*11
        c2 -= 11
        for i in range(3):
            if c2 > 10 :
                p2 = 10
            else:
                p2 = c2
            print(11, p2)
            c1 -= 11
            c2 -= p2
    else:
        # impossible
        print(-1, -1)
