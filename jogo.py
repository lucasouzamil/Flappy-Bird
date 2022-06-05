import pygame, random
from sys import exit

pygame.init()

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
FPS = 60

background = {'dia'  :  pygame.image.load('assets/sprites/background-day.png').convert(),
              'noite':  pygame.image.load('assets/sprites/background-night.png').convert()}
for key in background.keys():
    background[key] = pygame.transform.scale(background[key], (SCREEN_WIDTH, SCREEN_HEIGHT))

modobackground = 'dia'

GAMEON = True
while GAMEON:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMEON = False
            pygame.quit()
            exit()

    screen.blit(background[modobackground], (0,0))
    pygame.display.update()
    clock.tick(FPS)