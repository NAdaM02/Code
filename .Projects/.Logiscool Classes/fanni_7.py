"""puzzle = "computer science"
my_solution = "******** *******"
life = 10
correct_letters = []
incorrect_letters = []

while life > 0 and not(my_solution == puzzle):
    print(my_solution)
    guess = input("Guess a new letter:\n")
    if len(guess) == 1:
        benne_van = False
        for i in range(len(puzzle)):
            if puzzle[i] == guess:
                benne_van = True
                my_solution_list = list(my_solution)
                my_solution_list[i] = guess
                my_solution = "".join(my_solution_list)
        if benne_van == True:
            correct_letters.append(guess)
        else:
            incorrect_letters.append(guess)
            life -= 1
            print("You have " + str(life) + " lives left")
        print("Good guesses: " + str(correct_letters))
        print("Bad guesses: " + str(incorrect_letters))
    else:
        if guess == puzzle:
            my_solution = guess
        else:
            print("Bad guess")
            life -= 2
            print("You have " + str(life) + " lives left")
if life > 0:
    print("--You win--")
else:
    print("--You loose--")"""

"""x = int(input("X: "))
y = int(input("Y: "))

if x > 0 and y > 0:
    print("1")
if x < 0 and y > 0:
    print("2")
if x > 0 and y < 0:
    print("4")
if x < 0 and y < 0:
    print("3")"""

"""num1 = int(input("Első szám: "))
num2 = int(input("Második szám: "))

lnko = 1
for i in range(2,num1+1):
    if num1 % i == 0 and num2 % i == 0:
        lnko = i
print("A legnagyobb közös osztó: " + str(lnko))
print("A legkisebb közös többszörös: " + str(int(num1*num2/lnko)))"""

"""num = int(input("Add meg a számot: "))
prim_osztok = []
oszto = 2
while num > 1:
    if num % oszto == 0:
        num = num/oszto
        prim_osztok.append(oszto)
    else:
        oszto += 1
print(prim_osztok)"""
