print('Hello World!')
import pygame
pygame.init()
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
game=True
while game:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game=False
pygame.quit()