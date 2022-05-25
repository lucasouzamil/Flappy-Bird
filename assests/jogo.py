print('Hello World!')
from email.mime import image
import pygame
pygame.init()
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
game=True
maca_image=pygame.image.load('').convert()
class maca(pygame.sprite.Sprite):
       def __init__(self,):
            pygame.sprite.Sprite.__init__(self)
            self.image=maca_image
            self.rect = self.image.get_rect()
            self.rect.x = (300,300)
            self.rect.y =(300,300)
while game:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game=False
pygame.quit()