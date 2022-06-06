import pygame, random
from sys import exit

pygame.init()

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 750

#CONFIGURAÇÔES

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 750

VELOCIDADE_JOGO = -5

CHAO_ALTURA = 100

CANO_WIDTH  = 90
CANO_HEIGHT = 600
CANO_GAP_inicial = 180
CANO_GAP    = CANO_GAP_inicial
CANO_TAMNHOMINIMO = 30

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
    def __init__(self, posx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

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

class Cano(pygame.sprite.Sprite):
    def __init__(self, invertido):
        pygame.sprite.Sprite.__init__(self)

        self.cores = { 'verde':  pygame.transform.scale(pygame.image.load('assets/sprites/pipe-green.png').convert_alpha(), (CANO_WIDTH, CANO_HEIGHT)),
                       'vermelho':pygame.transform.scale(pygame.image.load('assets/sprites/pipe-red.png').convert_alpha(), (CANO_WIDTH, CANO_HEIGHT))}

        self.invertido = invertido
        self.cordocano = 'verde'
        self.image = self.cores[self.cordocano]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_HEIGHT-20
        self.posicaox = 0

        if self.invertido:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.left = canonormal.rect.left
            self.rect.bottom = canonormal.rect.top - CANO_GAP

        else:
            self.posicaox = random.randint(CANO_TAMNHOMINIMO+CANO_GAP, SCREEN_HEIGHT-CHAO_ALTURA-CANO_TAMNHOMINIMO)
            self.rect.top = self.posicaox


    def update(self):
        self.image = self.cores[self.cordocano]
        if self.invertido:
            self.image = pygame.transform.flip(self.image,False,True)
        self.movimentovertical()

    def movimentovertical(self):
        if self.invertido:
            self.rect.left = canonormal.rect.left
            self.rect.bottom = canonormal.rect.top - CANO_GAP
        else:
            self.rect.x += VELOCIDADE_JOGO
            if self.rect.right <= 0:
                self.rect.left = SCREEN_WIDTH
                self.posicaox =  random.randint(CANO_TAMNHOMINIMO+CANO_GAP, SCREEN_HEIGHT-CHAO_ALTURA-CANO_TAMNHOMINIMO)
            self.rect.top = self.posicaox

    def jogardenovo(self):
        if self.invertido:
            self.rect.left = canonormal.rect.left
            self.rect.bottom = canonormal.rect.top - CANO_GAP
        else:
            self.rect.left = SCREEN_HEIGHT-20
            self.posicaox = random.randint(CANO_TAMNHOMINIMO+CANO_GAP, SCREEN_HEIGHT-CHAO_ALTURA-CANO_TAMNHOMINIMO)
            self.rect.top = self.posicaox

#DECLARAÇÃO DOS GRUPOS DAS CLASSES E DOS OBJETOS

canos   = pygame.sprite.Group()
chaos   = pygame.sprite.Group()
all_sprites_jogando = pygame.sprite.Group()

canonormal = Cano(False)
canoinvert = Cano(True)

canos.add(canonormal)
canos.add(canoinvert)

all_sprites_jogando.add(canonormal)
all_sprites_jogando.add(canoinvert)

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