import pygame, random
from sys import exit

pygame.init()

#CONFIGURAÇÔES

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 750

VELOCIDADE_JOGO = -5

CHAO_ALTURA = 100

#ASSETS

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
FPS = 60

background = {'dia'  :  pygame.image.load('assets/sprites/background-day.png').convert(),
              'noite':  pygame.image.load('assets/sprites/background-night.png').convert()}
for key in background.keys():
    background[key] = pygame.transform.scale(background[key], (SCREEN_WIDTH, SCREEN_HEIGHT))

modobackground = 'dia'


#CLASSES

class Chao(pygame.sprite.Sprite):
    def _init_(self, posx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite._init_(self)

        self.chao_img = pygame.transform.scale(pygame.image.load('assets/sprites/base.png').convert_alpha(), (SCREEN_WIDTH, CHAO_ALTURA))
        self.image = self.chao_img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT
        self.rect.left = posx

    def update(self):
        self.rect.left += VELOCIDADE_JOGO
        if self.rect.right <= 0:
            self.rect.left = SCREEN_WIDTH



#DECLARAÇÃO DOS GRUPOS DAS CLASSES E DOS OBJETOS

chaos   = pygame.sprite.Group()
all_sprites_jogando = pygame.sprite.Group()

for i in range(2): 
    if i == 0:
        chao = Chao(0)
    else:
        chao = Chao(SCREEN_WIDTH)
    chaos.add(chao)
    all_sprites_jogando.add(chao)


# LOOPING GAME

GAMEON = True
while GAMEON:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMEON = False
            pygame.quit()
            exit()

    screen.blit(background[modobackground], (0,0))

    all_sprites_jogando.update()
    all_sprites_jogando.draw(screen)

    pygame.display.update()
    clock.tick(FPS)