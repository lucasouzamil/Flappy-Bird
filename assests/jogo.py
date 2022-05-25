from email.mime import image
import pygame, random
from sys import exit

pygame.init()

TAMCELULAS = 40
qntdCEL_x = 35
qntdCEL_y = 20

celula = pygame.Surface((TAMCELULAS,TAMCELULAS))
celula.fill((158, 179, 152))
window = pygame.display.set_mode((qntdCEL_x*TAMCELULAS, qntdCEL_y*TAMCELULAS))
game=True

def desenhacampo(cellsize,qntdx,qntdy,cel):

    for celulax in range(qntdx):
        for celulay in range(qntdy):
            window.blit(cel,(celulax*cellsize,celulay*cellsize))

class maca(pygame.sprite.Sprite):
       def __init__(self,):
            pygame.sprite.Sprite.__init__(self)
            self.rect.x = (300,300)
            self.rect.y =(300,300)
  
while game:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.exit()
            exit()
    desenhacampo(TAMCELULAS,qntdCEL_x,qntdCEL_y,celula)
    window.fill((255,255,255))
    #desenhacampo(TAMCELULAS,qntdCEL_x,qntdCEL_y)
pygame.quit()