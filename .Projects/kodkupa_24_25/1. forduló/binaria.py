temak_szama = int(input())
konyvek_szamai = tuple(map(int, input().split()))

def get_missing_number(x):
    a = 0
    i = 1
    while a < x:
        a += i
        i *= 2
    return a - x

hianyzo_konyvek_szama = sum((get_missing_number(konyvek_szama) for konyvek_szama in konyvek_szamai))

print(hianyzo_konyvek_szama)
