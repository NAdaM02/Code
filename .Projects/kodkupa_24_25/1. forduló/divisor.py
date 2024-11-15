import math
def divisor_generator(n):
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield int(divisor)

def get_next_prime(number):
    n = number
    while True:
        n += 1
        is_prime = True
        for _d in range(2, int((n**(1/2)))+1):
            if n % _d == 0:
                is_prime = False
                break

        if is_prime:  return n

def count_in_list(c_list, element):
    count = 0
    for list_element in c_list:
        if element == list_element:
            count += 1
    return count



szamharmasok_szama = int(input())

szamharmasok = []

for i in range(szamharmasok_szama):
    A, B, K = input().split()
    A, B, K = int(A), int(B), int(K)
    szamharmasok.append((A, B, K))

for szamharmas in szamharmasok:
    primes = []
    A = szamharmas[0]
    B = szamharmas[1]
    K = szamharmas[2]

    ABK = sum(szamharmas)

    divisors = divisor_generator(ABK)
    
    biggest_common_d = 1
    for d in divisors:
        if d != ABK:
            a = 0 if A % d == 0 else d - A%d
            b = 0 if B % d == 0 else d - B%d

            if (a+b <= K) and (biggest_common_d < d):
                biggest_common_d = d
    
    print(biggest_common_d)
