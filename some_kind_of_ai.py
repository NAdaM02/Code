import sys
import pygame
import random
import math

pygame.init()
myVector = pygame.math.Vector2
height = 800
width = 800
FPS = 60
frame_per_second = pygame.time.Clock()
display_surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('AI')

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)

gen = 0
target_x = 0
target_y = 0
pointer_x = width // 2
pointer_y = height // 2
w_1, w_2, w_3, w_4 = 1,1,1,1
ID = target_x*w_1+target_y*w_2+pointer_x*w_3+pointer_y*w_4

font = pygame.font.Font('freesansbold.ttf', 16)
text = font.render(('Gen: '+str(gen)+'   ID: '+str(ID)), True, white, blue)
textRect = text.get_rect()
textRect.center = (30, 10)

def NewTarget():
    global target_x, target_y
    target_x = random.randint(0, width)
    target_y = random.randint(0, height)

def NewGen():
    for i in range(10):
        print(0)



while True:
    for event in pygame.event.get():
        # Quitting game
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()
    # Clear screen
    display_surface.fill(black)

    NewGen()


    display_surface.blit(text, textRect)


    # Update and tick screen
    pygame.display.update()
    frame_per_second.tick(FPS)
