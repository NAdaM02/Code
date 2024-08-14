"""import emoji

a = 5
print(emoji.emojize(f'Python is a {a} :star2: language.', language='alias'))
print(emoji.emojize(':lion: :crown:', language='alias'))
print(emoji.emojize(':monkey: :genie: :princess: :heart: :man:', language='alias'))
print(emoji.emojize(':girl: :heart: :ogre: :rose: :prince:', language='alias'))
print(emoji.emojize(':princess: :pick: :pick: :pick: :pick: :pick: :pick: :pick: :apple:', language='alias'))
print(emoji.emojize(f'Python is a {a} :star2: language.', language='alias'))
print(emoji.demojize("⛏"))"""
import random

"""from art import *
a = 7
tprint(f'Logiscool is {a} years old.')"""

"""import pyjokes as pj
print(pj.get_joke())"""

"""Guess a number within a range.

Exercises

1. Change the range to be from 0 to 1,000,000.
2. Can you still guess the number?
3. Print the number of guesses made.
4. Limit the number of guesses to the minimum required.
"""

"""from random import randint

start = 0
end = 1000000
value = randint(start, end)
min_required = end/2-2

print(value)
print("I'm thinking of a number between", start, 'and', end)

guess = None
sum = 0
while guess != value and sum <= min_required:
    text = input('Guess the number: ')
    guess = int(text)
    sum+=1
    if guess < value:
        print('Higher.')
    elif guess > value:
        print('Lower.')
if(sum > 1):
    print('You guessed correctly in',sum,'attempts.')
else:
    print('You guessed correctly in', sum, 'attempt. Without cheating the chances were',1/(end-start))"""

"""Tiles, number swapping game.

Exercises

1. Track a score by the number of tile moves.
2. Permit diagonal squares as neighbors.
3. Respond to arrow keys instead of mouse clicks.
4. Make the grid bigger.
"""



from random import *
from turtle import *

from freegames import floor, vector

score = 0

tiles = {}
neighbors = [
    vector(200, 0),
    vector(-200, 0),
    vector(0, 200),
    vector(0, -200),
]


def load():
    """Load tiles and scramble."""
    count = 1

    for y in range(-400, 400, 200):
        for x in range(-400, 400, 200):
            mark = vector(x, y)
            tiles[mark] = count
            count += 1

    tiles[mark] = None

    for count in range(1000):
        neighbor = choice(neighbors)
        spot = mark + neighbor

        if spot in tiles:
            number = tiles[spot]
            tiles[spot] = None
            tiles[mark] = number
            mark = spot


def square(mark, number):
    """Draw white square with black outline and number."""
    up()
    goto(mark.x, mark.y)
    down()

    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(198)
        left(90)
    end_fill()

    if number is None:
        return
    elif number < 10:
        forward(20)

    write(number, font=('Arial', 60, 'normal'))


def tap(x, y):
    global score
    """Swap tile and empty square."""
    x = floor(x, 200)
    y = floor(y, 200)
    mark = vector(x, y)

    for neighbor in neighbors:
        spot = mark + neighbor

        if spot in tiles and tiles[spot] is None:
            score += 1
            number = tiles[mark]
            tiles[spot] = number
            square(spot, number)
            tiles[mark] = None
            square(mark, None)
            print("\n" * 40,score)


def draw():
    """Draw all tiles."""
    for mark in tiles:
        square(mark, tiles[mark])
    update()


"""setup(420, 420, 370, 0)
hideturtle()
tracer(False)
load()
draw()
onscreenclick(tap)
done()"""



"""Cannon, hitting targets with projectiles.

Exercises

1. Keep score by counting target hits.
2. Vary the effect of gravity.
3. Apply gravity to the targets.
4. Change the speed of the ball.
"""

from random import randrange
from turtle import *

from freegames import vector

ball = vector(-200, -200)
speed = vector(0, 0)
targets = []


def tap(x, y):
    """Respond to screen tap."""
    if not inside(ball):
        ball.x = -199
        ball.y = -199
        speed.x = (x + 200) / 25
        speed.y = (y + 200) / 25


def inside(xy):
    """Return True if xy within screen."""
    return -200 < xy.x < 200 and -200 < xy.y < 200


def draw():
    """Draw ball and targets."""
    clear()

    for target in targets:
        goto(target.x, target.y)
        dot(20, 'blue')

    if inside(ball):
        goto(ball.x, ball.y)
        dot(6, 'red')

    update()

hits = 0
def move():
    global hits
    """Move ball and targets."""
    if randrange(40) == 0:
        y = randrange(-150, 150)
        target = vector(200, y)
        targets.append(target)

    for target in targets:
        target.x -= 0.5

    if inside(ball):
        speed.y -= randrange(30,40)*0.01
        ball.move(speed)

    dupe = targets.copy()
    targets.clear()

    for target in dupe:
        if abs(target - ball) > 13:
            targets.append(target)
        else:
            hits += 1
            print("\n" * 40, hits)

    draw()

    for target in targets:
        if not inside(target):
            return

    ontimer(move, 50)


setup(420, 420, 370, 0)
hideturtle()
up()
tracer(False)
onscreenclick(tap)
move()
done()
