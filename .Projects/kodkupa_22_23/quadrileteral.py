def Max4(_list):
    count_dict = {}
    result = []
    for item in _list:
        if count_dict.get(item, 0) < 4:
            result.append(item)
            count_dict[item] = count_dict.get(item, 0) + 1
    return result

def Search():
    found = False
    rod_num = int(input())
    rods = list(map(int, input().split()))
    rods.sort(reverse=True)
    rods = Max4(rods)
    for a in range(rod_num-4+1):
        for b in range(a+1, rod_num-3+1):
            for c in range(b+1, rod_num-2+1):
                for d in range(c+1, rod_num-1+1):
                    _a = rods[a]
                    _b = rods[b]
                    _c = rods[c]
                    _d = rods[d]
                    if _a+_b+_c > _d and _a+_c+_d > _b and _a+_c+_d > _b and _a+_b+_d > _c and _b+_c+_d > _a :
                        print(_a,_b,_c,_d)
                        found = True
                        return 0
    if not found :
        print(-1)

Search()
