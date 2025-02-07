
N = int(input())

counts = [0 for i in range(10)]

for num in range(1, N + 1):
    while num > 0:
        counts[num % 10] += 1
        num //= 10

print(" ".join(map(str, counts)))
