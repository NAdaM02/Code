

def Integrate_Data():
    f = open('data.txt', "r", encoding="utf-8")
    content = f.read()
    data = []
    rows = []
    row = ''
    for c in content:
        if c == '\n':
            rows.append(row)
            row = ''
        else:
            row += c
    for r in rows:
        d = r.split()
        for v in range(len(d)-1):
            d[v] = int(d[v])
        d = (tuple([i for i in d[:-1]]),[d[-1]])
        data.append(d)
    return data
data = Integrate_Data()
print(data)
