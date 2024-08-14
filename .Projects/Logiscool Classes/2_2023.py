import pygame
import random
import sys
import time

pygame.init()
pygame.font.init()

myVector = pygame.math.Vector2
height = 450
width = 400
# Setting acceleration and smoothing
acc = 0.5
smoothing = 0.12
# Set default values here
smoothing *= -1
FPS = 60
# Initalise
frame_per_second = pygame.time.Clock()
display_surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('*The caption goes here*')


# P L A Y E R  c l a s s
class Player(pygame.sprite.Sprite):
    # player's __init__ function
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(10, 420))

        self.pos = myVector((10, 385))
        self.v = myVector(0, 0)
        self.a = myVector(0, 0)
        self.score = 0
        self.jumping = False

    # player's Move function
    def Move(self):
        self.a = myVector(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
        if (pressed_keys[pygame.K_a]):
            self.a.x = -acc
        elif (pressed_keys[pygame.K_d]):
            self.a.x = acc
        self.a.x += self.v.x * smoothing
        self.v += self.a
        self.pos += self.v + 0.5 * self.a
        if (self.pos.x < -15):
            self.pos.x = width+15
        if (self.pos.x > width+15):
            self.pos.x = -15
        self.rect.midbottom = self.pos

    # player's Update function
    def Update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if (hits and P1.v.y > 0):
            self.pos.y = hits[0].rect.top + 1
            self.v.y = 0
            self.jumping = False
        self.rect.midbottom = self.pos

    # player's Jump function
    def Jump(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if (hits and not self.jumping):
            self.jumping = True
            self.v.y = -15

    # player's Cancel Jump function
    def CancelJump(self):
        if (self.jumping):
            if (self.v.y < -3):
                self.v.y = -3


# P L A T F O R M  c l a s s
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100),12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0, width-10), random.randint(0, height-30)))
        self.speed = random.randint(-1,1)
        self.moving = True

    # platform's Move function
    def Move(self):
        hits = self.rect.colliderect(P1.rect)
        if (self.moving):
            self.rect.move_ip(self.speed, 0)
            if (hits):
                P1.pos += (self.speed, 0)
            if (self.speed > 0 and self.rect.left > width):
                self.rect.right = 0
            if (self.speed < 0 and self.rect.right < 0):
                self.rect.left = width

# Platform generation
def PlatformGenerator():
    while (len(platforms) < 7):
        w = random.randint(50, 100)
        c = True
        while (c):
            p = Platform()
            p.rect.center = (random.randrange(0, width - w), random.randrange(-50, 0)) #utolsó 0 helyett -12
            c = Check(p,platforms)
        platforms.add(p)
        all_sprites.add(p)

# Check if platform's not too close to other platforms
def Check(platform, groupies):
    if (pygame.sprite.spritecollideany(platform, groupies)):
        return True
    else:
        for plat in groupies:
            if (plat == platform):
                continue
            if (abs(platform.rect.top - plat.rect.bottom) < 50 and abs(platform.rect.bottom - plat.rect.top < 50)):
                return True

# Set default sprites
PT1 = Platform()
PT1.surf = pygame.Surface((width,20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center=(width//2, height-10))
PT1.moving = False
P1 = Player()
# Add sprites to groups
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(PT1)
platforms = pygame.sprite.Group()
platforms.add(PT1)

# Create 5 to 6 platforms
for x in range(random.randint(5,6)):
    C = True
    while C:
        pl = Platform()
        C = Check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)

# Main game loop
while True:
    for event in pygame.event.get():
        # Quitting game
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        # Detect jumping
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_SPACE:
                P1.Jump()
        # Cancel jumping
        if (event.type == pygame.KEYUP):
            if event.key == pygame.K_SPACE:
                P1.CancelJump()
    # Clear screen
    display_surface.fill((0,0,0))
    # Display score
    f = pygame.font.SysFont('Verdena', 20)
    g = f.render(str(P1.score), True, (255, 255, 255))
    display_surface.blit(g, (width//2 - g.get_width()//2, 10))
    # Make a follow-cam like effect by moving platforms accordingly
    if (P1.rect.top <= height/3):
        P1.pos.y += abs(P1.v.y)
        for plat in platforms:
            plat.rect.y += abs(P1.v.y)
            if (plat.rect.top >= height):
                P1.score += 1
                plat.kill()
    # Lose
    if P1.rect.top > height:
        for entity in all_sprites:
            entity.kill()
            time.sleep(0.4)
            display_surface.fill((255,0,0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()
    # Move and update player
    P1.Update()
    # Platform generation
    PlatformGenerator()
    # Display sprites
    for entity in all_sprites:
        display_surface.blit(entity.surf, entity.rect)
        entity.Move()
    # Update and tick screen
    pygame.display.update()
    frame_per_second.tick(FPS)
