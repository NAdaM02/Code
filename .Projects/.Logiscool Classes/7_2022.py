# Téglapiramis
"""bricks = int(input('How many bricks do you want to build the pyramid out of? '))
height = 0

while (bricks > 0):
    if (height+1 <= bricks):
        bricks -= height + 1
        height += 1
    else:
        break
print(f'Pyramid height: {height}')
if(bricks > 0):
    print(f'Bricks left: {bricks}')"""


# Logikai operátorok
"""x = 10
print(x > 10)
print(not (x > 10))
print(x % 2 == 0 and x % 3 > 0)
print(not (x % 3 == 0) or x < 10)"""

# De Morgan azonosság
"""p = False
q = True
print(not (p and q) == (not p or not q))
print(not (p or q) == (not p and not q))"""

# Bitenkénti azonosság
"""num_1 = 42  #101010
num_2 = 36  #100100
print(bin(num_1 & num_2))  #100000
print(bin(num_1 | num_2))  #101110
print(bin(num_1 ^ num_2))  #001110"""

# Bit shiftelés
"""num_1 = 42
num_2 = 63
# Balra shift   -> 2x
# Jobbra shift  -> x/2
# n << x -> n * 2**x
# n >> x -> n / 2**x

num_1 >>= 1
print(num_1)
num_2 <<= 2
print(num_2)"""

# Műveleti sorrend
# 0. +-~
# 1. **
# 2. * / // %
# 3. + -
# 4. << >>
# 5. < <= > >=
# 6. == !=
# 7. &
# 8. |
# 9. = += -= *= >>= stb. (értékadók)
# 10. not
# 11. and
# 12. or


"""age_income = {"Joe": [32, 14500],
              "Emily": [27, 13000],
              "George": [58, 22000],
              "Michael": [42, 27000],
              "Lois": [39, 23000]
              }

# Legfiatalabb:
x = list(age_income.values())[0][0]
for e in age_income:
    if age_income[e][0]>x:
        age = age_income[e][0]
        youngest = e
print("Youngest:", youngest, ", age:", age)

# Átlag életkor:
avg = 0
for i in age_income.values():
    avg += i[0]
avg /= len(age_income)
print('The average age in the company is ', avg, '.', sep='')"""


inp = input('Give me an input\n')
list_of_inputs = inp.split(',')
for i in range(len(list_of_inputs)):
    list_of_inputs[i] = float(list_of_inputs[i])
    list_of_inputs[i] = int(list_of_inputs[i])
print(list_of_inputs)
