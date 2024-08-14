import pygame
import random

pygame.init()
dis = pygame.display.set_mode((800,600))

blue = (0,0,255)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)

x1 = 300
y1 = 300

x1_change = 0
y1_change = 0

snakelength = 1
snake = []

foodx = random.randrange(10, 790, 10)
foody = random.randrange(10, 390, 10)

clock = pygame.time.Clock()

pygame.display.update()
pygame.display.set_caption('Snake')
game_over = False
while (not game_over):
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            game_over = True

        if(event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_a):
                x1_change = -10
                y1_change = 0
            if (event.key == pygame.K_d):
                x1_change = 10
                y1_change = 0
            if (event.key == pygame.K_s):
                x1_change = 0
                y1_change = 10
            if (event.key == pygame.K_w):
                x1_change = 0
                y1_change = -10

    x1 += x1_change
    y1 += y1_change
    head = [x1,y1]
    snake.append(head)
    if (len(snake) > snakelength):
        del snake[0]

    dis.fill(white)
    pygame.draw.rect(dis, red, [foodx, foody, 10, 10])
    pygame.draw.rect(dis, blue, [x1,y1,10,10])

    for item in snake:
        pygame.draw.rect(dis, blue, [item[0], item[1], 10, 10])

    if (foodx == x1 and foody == y1):
        snakelength += 1
        foodx = random.randrange(10, 790, 10)
        foody = random.randrange(10, 390, 10)

    if (x1 < 0 or x1 > 800 or y1 < 0 or y1 > 600):
        game_over = True

    for item in snake[:-1]:
        if(item == head):
            game_over = True
            break

    pygame.display.update()
    clock.tick(15)

pygame.quit()
quit()
