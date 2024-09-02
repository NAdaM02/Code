N = int(input())
example = ''
if (N == 1):
    example = -1
else:
    if N % 2 == 1 :
        example += '111'
        N -= 3
    example += int(N/2)*'15'
print(example)
