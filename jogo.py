import pygame, random
from sys import exit

pygame.init()

#CONFIGURAÇÔES

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 750

PERIQUITO_WIDTH  = 45
PERIQUITO_HEIGHT = PERIQUITO_WIDTH * (13/18)


SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 750

VELOCIDADE_JOGO = -5

CHAO_ALTURA = 100

CANO_WIDTH  = 90
CANO_HEIGHT = 600
CANO_GAP_inicial = 180
CANO_GAP    = CANO_GAP_inicial
CANO_TAMNHOMINIMO = 30

VELOCIDADE_JOGO = 0
VELOCIDADE_YLIMITE = 7
intensidadesalto = 12
GRAVIDADEIDEAL = 0.5
GRAVIDADE = 0

PONTUACAO = 0

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

inicio_img = pygame.image.load('assets/sprites/message.png').convert_alpha()
inicio_imgx = 0.4*SCREEN_HEIGHT
inicio_imgy = 1.5*inicio_imgx
inicio_img = pygame.transform.scale(inicio_img, (inicio_imgx, inicio_imgy))
gameover_img = pygame.image.load('assets/sprites/gameovercompleto.png').convert_alpha()
tamanhogameoverx = SCREEN_WIDTH*0.5
tamanhogameovery = tamanhogameoverx*1.2
gameover_img = pygame.transform.scale(gameover_img, (tamanhogameoverx, tamanhogameovery))
pontos_widht = 0.15*tamanhogameoverx
pontos_height = 1.7 * pontos_widht
numbers = {}
for i in range(10):
    numbers[i] = pygame.transform.scale(pygame.image.load(f'assets/sprites/{i}.png').convert_alpha(), (pontos_widht, pontos_height))


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

class Periquito(pygame.sprite.Sprite):
    def __init__(self):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.cores = { 'amarelo':[pygame.transform.scale(pygame.image.load('assets/sprites/yellowbird-downflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT)),
                                  pygame.transform.scale(pygame.image.load('assets/sprites/yellowbird-midflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT)),
                                  pygame.transform.scale(pygame.image.load('assets/sprites/yellowbird-upflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT)),
                                  pygame.transform.scale(pygame.image.load('assets/sprites/yellowbird-midflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT))],
                       'vermelho':[pygame.transform.scale(pygame.image.load('assets/sprites/redbird-downflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT)),
                                  pygame.transform.scale(pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT)),
                                  pygame.transform.scale(pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT)),
                                  pygame.transform.scale(pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT))],
                           'azul':[pygame.transform.scale(pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT)),
                                  pygame.transform.scale(pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT)),
                                  pygame.transform.scale(pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT)),
                                  pygame.transform.scale(pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(), (PERIQUITO_WIDTH, PERIQUITO_HEIGHT))]}

        self.impulso_snd = pygame.mixer.Sound('assets/snd/impulse.wav')
        self.crashing_snd = pygame.mixer.Sound('assets/snd/crashing.wav')
        self.falling_snd = pygame.mixer.Sound('assets/snd/falling.wav')
        self.point_snd =  pygame.mixer.Sound('assets/snd/point.wav')

        self.alternadordoperiquito = 0
        self.cordoperiquito = 'amarelo'
        self.image = self.cores[self.cordoperiquito][self.alternadordoperiquito]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 4
        self.rect.centery = SCREEN_HEIGHT /2
        self.speedx = 0
        self.speedy = 0

        self.verificaponto = 0
        self.saltopermitido = True
        self.alternaimagempermitida = True
        self.ultimatroca = pygame.time.get_ticks()
        self.tempodetroca = 100

    def update(self):
        self.movimentovertical()
        self.alternaimagem()
        #self.rotacaoperiquito() 
        self.colisaocomcanos()
        self.colisaocomchao()
        self.contaponutacao()

    def movimentovertical(self):
        self.speedy += GRAVIDADE
        if self.speedy <= -VELOCIDADE_YLIMITE:
            self.speedy = -VELOCIDADE_YLIMITE
        self.rect.centery += self.speedy
        return

    def jump(self, intensidadesalto):
        if self.saltopermitido:
            self.impulso_snd.play() 
            self.speedy -= intensidadesalto

    # def rotacaoperiquito(self):
    #     angulo = (self.speedy*-80)/VELOCIDADE_YLIMITE
    #     self.image = pygame.transform.rotate(self.image,angulo)

    def alternaimagem(self):
        agora = pygame.time.get_ticks()
        if self.alternaimagempermitida:
            if agora - self.ultimatroca >= self.tempodetroca:
                self.ultimatroca =  pygame.time.get_ticks()
                self.alternadordoperiquito += 1
                if self.alternadordoperiquito > 3:
                    self.alternadordoperiquito = 0
            self.image = self.cores[self.cordoperiquito][self.alternadordoperiquito]

    def colisaocomcanos(self):
        global VELOCIDADE_JOGO
        for sprite in canos:
            if VELOCIDADE_JOGO != 0:
                if sprite.rect.colliderect(self.rect):
                    VELOCIDADE_JOGO = 0
                    self.crashing_snd.play()
                    self.falling_snd.play()
                    self.saltopermitido = False
                    self.alternaimagempermitida = False

    def colisaocomchao(self):
        global VELOCIDADE_JOGO,GRAVIDADE, state_game
        for sprite in chaos:
            if sprite.rect.colliderect(self.rect):
                if VELOCIDADE_JOGO != 0:
                    self.crashing_snd.play()
                    self.rect.bottom = sprite.rect.top
                    self.saltopermitido = False
                    self.alternaimagempermitida = False
                else:
                    self.crashing_snd.play()
                    self.rect.bottom = sprite.rect.top
                    self.saltopermitido = False
                    self.alternaimagempermitida = False
                gameover()

    def contaponutacao(self):
        global PONTUACAO,CANO_GAP
        if (player.rect.right - canonormal.rect.left > 1 and player.rect.right - canonormal.rect.left < 10) and self.verificaponto ==0: 
            self.verificaponto = 1
        elif (player.rect.right - canonormal.rect.right > 1) and self.verificaponto ==1: 
            self.verificaponto = 0
            self.point_snd.play()
            CANO_GAP-= 1
            PONTUACAO +=1

    def jogardenovo(self):
        self.saltopermitido = True
        self.alternaimagempermitida = True
        self.rect.centerx = SCREEN_WIDTH / 4
        self.rect.centery = SCREEN_HEIGHT /2

class Menu(pygame.sprite.Sprite):
    def __init__(self):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        menu_img = pygame.image.load('assets/sprites/menucompletoletras.png').convert_alpha()
        tamanhopainelx = SCREEN_WIDTH*0.6
        tamanhopainely = tamanhopainelx
        menu_img = pygame.transform.scale(menu_img, (tamanhopainelx, tamanhopainely))

        self.click_sound =  pygame.mixer.Sound('assets/snd/point.wav')
        self.image = menu_img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

    def periquitoamarelo(self):
        player.cordoperiquito = 'amarelo'
        self.click_sound.play()
    def periquitovermelho(self):
        player.cordoperiquito = 'vermelho'
        self.click_sound.play()
    def periquitoazul(self):
        player.cordoperiquito = 'azul'
        self.click_sound.play()
    def periquitohumberto(self):
        player.cordoperiquito = 'humberto'
        self.click_sound.play()
    def canovermelho(self):
        canonormal.cordocano = 'vermelho'
        canoinvert.cordocano = 'vermelho'
        self.click_sound.play()
    def canoverde(self):
        canonormal.cordocano = 'verde'
        canoinvert.cordocano = 'verde'
        self.click_sound.play()
    def dia(self):
        global modobackground
        modobackground = 'dia'
        self.click_sound.play()
    def noite(self):
        global modobackground
        modobackground = 'noite'
        self.click_sound.play()

#FUNCOES

def mostrapontosgameover():
    pontosstr = str(PONTUACAO)
    if state_game == 'gameover':
        if  len(pontosstr) == 1:
            screen.blit(numbers[int(pontosstr[0])],(SCREEN_WIDTH/2 - pontos_widht/2 , SCREEN_HEIGHT/2 - 0.25*tamanhogameovery))
        elif len(pontosstr) == 2:
            screen.blit(numbers[int(pontosstr[1])],(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 0.25*tamanhogameovery))
            screen.blit(numbers[int(pontosstr[0])],(SCREEN_WIDTH/2 - pontos_widht, SCREEN_HEIGHT/2 - 0.25*tamanhogameovery))
        elif len(pontosstr) == 3:
            screen.blit(numbers[int(pontosstr[2])],(SCREEN_WIDTH/2 + pontos_widht/2 , SCREEN_HEIGHT/2 - 0.25*tamanhogameovery))
            screen.blit(numbers[int(pontosstr[1])],(SCREEN_WIDTH/2 - pontos_widht/2, SCREEN_HEIGHT/2 - 0.25*tamanhogameovery))
            screen.blit(numbers[int(pontosstr[0])],(SCREEN_WIDTH/2 - pontos_widht-pontos_widht/2 , SCREEN_HEIGHT/2 - 0.25*tamanhogameovery))

    elif state_game == 'jogando':
        if  len(pontosstr) == 1:
            screen.blit(numbers[int(pontosstr[0])],(SCREEN_WIDTH/2-pontos_widht/2,SCREEN_HEIGHT/15))
        elif len(pontosstr) == 2:
            screen.blit(numbers[int(pontosstr[1])],(SCREEN_WIDTH/2,SCREEN_HEIGHT/15))
            screen.blit(numbers[int(pontosstr[0])],(SCREEN_WIDTH/2-pontos_widht,SCREEN_HEIGHT/15))
        elif len(pontosstr) == 3:
            screen.blit(numbers[int(pontosstr[2])],(SCREEN_WIDTH/2+0.5*pontos_widht,SCREEN_HEIGHT/15))
            screen.blit(numbers[int(pontosstr[1])],(SCREEN_WIDTH/2-pontos_widht/2,SCREEN_HEIGHT/15))
            screen.blit(numbers[int(pontosstr[0])],(SCREEN_WIDTH/2-1.5*pontos_widht,SCREEN_HEIGHT/15))

def gameover():
    global state_game, VELOCIDADE_JOGO, GRAVIDADE

    state_game = 'gameover'
    player.saltopermitido = False
    player.alternaimagempermitida = False
    VELOCIDADE_JOGO = 0
    GRAVIDADE = 0

def gameback():
    global PONTUACAO, state_game, CANO_GAP, CANO_GAP_inicial

    state_game = 'jogando'
    player.saltopermitido = True
    player.alternaimagempermitida = True
    player.rect.centerx = SCREEN_WIDTH / 4
    player.rect.centery = SCREEN_HEIGHT /2
    player.speedx = 0
    player.speedy = 0

    canonormal.rect.left = SCREEN_HEIGHT-20
    canonormal.posicaox = random.randint(CANO_TAMNHOMINIMO+CANO_GAP, SCREEN_HEIGHT-CHAO_ALTURA-CANO_TAMNHOMINIMO)
    canonormal.rect.top = canonormal.posicaox

    canoinvert.rect.left = canonormal.rect.left
    canoinvert.rect.bottom = canonormal.rect.top - CANO_GAP

    CANO_GAP = CANO_GAP_inicial
    PONTUACAO = 0

#DECLARAÇÃO DOS GRUPOS DAS CLASSES E DOS OBJETOS

canos   = pygame.sprite.Group()
chaos   = pygame.sprite.Group()
players = pygame.sprite.Group()
all_sprites_jogando = pygame.sprite.Group()

player = Periquito()
canonormal = Cano(False)
canoinvert = Cano(True)

menu = Menu()
menus = pygame.sprite.Group()
menus.add(menu)

players.add(player)
canos.add(canonormal)
canos.add(canoinvert)

all_sprites_jogando.add(canonormal)
all_sprites_jogando.add(canoinvert)
all_sprites_jogando.add(player)

for i in range(2): 
    if i == 0:
        chao = Chao(0)
    else:
        chao = Chao(SCREEN_WIDTH)
    chaos.add(chao)
    all_sprites_jogando.add(chao)


# LOOPING GAME
state_game = 'start'
GAMEON = True
while GAMEON:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMEON = False
            pygame.quit()
            exit()
        #COMANDOS COM TECLADO
        if event.type == pygame.KEYDOWN:
            if state_game == 'jogando':
                if event.key == pygame.K_SPACE:
                    player.jump(intensidadesalto)
                    VELOCIDADE_JOGO = -5
                    GRAVIDADE = GRAVIDADEIDEAL
            if state_game == 'gameover':
                if event.key == pygame.K_SPACE:
                    gameback()
                if event.key == pygame.K_m:
                    state_game = 'menu'
            if state_game == 'start':
                if event.key == pygame.K_SPACE:
                    state_game = 'menu'
            if state_game == 'menu':
                if event.key == pygame.K_g:
                    menu.canoverde()
                if event.key == pygame.K_v:
                    menu.canovermelho()
                if event.key == pygame.K_d:
                    menu.dia()
                if event.key == pygame.K_n:
                    menu.noite()
                if event.key == pygame.K_1:
                    menu.periquitoamarelo()
                if event.key == pygame.K_2:
                    menu.periquitovermelho()
                if event.key == pygame.K_3:
                    menu.periquitoazul()
                if event.key == pygame.K_h:
                    menu.periquitohumberto()
                if event.key == pygame.K_ESCAPE:
                    gameback()
                    state_game = 'jogando'

    if state_game == 'start':
        screen.blit(background[modobackground], (0,0))
        screen.blit(inicio_img,(SCREEN_WIDTH/2-inicio_imgx/2,SCREEN_HEIGHT/2-inicio_imgy/2))

    if state_game == 'jogando':
        screen.blit(background[modobackground], (0,0))
        all_sprites_jogando.update()
        all_sprites_jogando.draw(screen)
        mostrapontosgameover()

    if state_game == 'menu':
        screen.blit(background[modobackground], (0,0))
        menus.update()
        menus.draw(screen)

    if state_game == 'gameover':
        screen.blit(background[modobackground], (0,0))
        screen.blit(gameover_img, (SCREEN_WIDTH/2-tamanhogameoverx/2, SCREEN_HEIGHT/2-tamanhogameovery/2))
        mostrapontosgameover()

    pygame.display.update()
    clock.tick(FPS)