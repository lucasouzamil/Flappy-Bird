""" 
import pygame, random
from assets import *
from configs import *

#CLASSES

class Chao(pygame.sprite.Sprite):
    def __init__(self, posx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.chao_mask = pygame.transform.scale(pygame.image.load(chao_img).convert_alpha(), (SCREEN_WIDTH, CHAO_ALTURA))
        self.image = self.chao_mask
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

        self.cores = { 'verde':  pygame.transform.scale(pygame.image.load(cano_verde_img).convert_alpha(), (CANO_WIDTH, CANO_HEIGHT)),
                                    'vermelho':pygame.transform.scale(pygame.image.load(cano_vermelho_img).convert_alpha(), (CANO_WIDTH, CANO_HEIGHT))}

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
            self.rect.bottom = canonormal.rect.top - cano_gap

        else:
            self.posicaox = random.randint(CANO_TAMNHOMINIMO+cano_gap, SCREEN_HEIGHT-CHAO_ALTURA-CANO_TAMNHOMINIMO)
            self.rect.top = self.posicaox


    def update(self):
        self.image = self.cores[self.cordocano]
        if self.invertido:
            self.image = pygame.transform.flip(self.image,False,True)
        self.movimentovertical()

    def movimentovertical(self):
        if self.invertido:
            self.rect.left = canonormal.rect.left
            self.rect.bottom = canonormal.rect.top - cano_gap
        else:
            self.rect.x += VELOCIDADE_JOGO
            if self.rect.right <= 0:
                self.rect.left = SCREEN_WIDTH
                self.posicaox =  random.randint(CANO_TAMNHOMINIMO+cano_gap, SCREEN_HEIGHT-CHAO_ALTURA-CANO_TAMNHOMINIMO)
            self.rect.top = self.posicaox

    def jogardenovo(self):
        if self.invertido:
            self.rect.left = canonormal.rect.left
            self.rect.bottom = canonormal.rect.top - cano_gap
        else:
            self.rect.left = SCREEN_HEIGHT-20
            self.posicaox = random.randint(CANO_TAMNHOMINIMO+cano_gap, SCREEN_HEIGHT-CHAO_ALTURA-CANO_TAMNHOMINIMO)
            self.rect.top = self.posicaox


class Periquito(pygame.sprite.Sprite):
    def __init__(self):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.cores = { 'amarelo':[pygame.transform.scale(yellow_downflap_mask, PERIQUITO_SIZE),
                                                            pygame.transform.scale(yellow_midflap_mask, PERIQUITO_SIZE),
                                                            pygame.transform.scale(yellow_upflap_mask, PERIQUITO_SIZE),
                                                            pygame.transform.scale(yellow_midflap_mask, PERIQUITO_SIZE)],
                                    'vermelho':[pygame.transform.scale(red_downflap_mask, PERIQUITO_SIZE),
                                                            pygame.transform.scale(red_midflap_mask, PERIQUITO_SIZE),
                                                            pygame.transform.scale(red_upflap_mask, PERIQUITO_SIZE),
                                                            pygame.transform.scale(red_midflap_mask, PERIQUITO_SIZE)],
                                                'azul':[pygame.transform.scale(blue_downflap_mask, PERIQUITO_SIZE),
                                                            pygame.transform.scale(blue_midflap_mask, PERIQUITO_SIZE),
                                                            pygame.transform.scale(blue_upflap_mask, PERIQUITO_SIZE),
                                                            pygame.transform.scale(blue_midflap_mask, PERIQUITO_SIZE)],
                                 'humberto':[pygame.transform.scale(humb_downflap_mask, (PERIQUITO_WIDTH, PERIQUITO_WIDTH*1.3)),
                                                            pygame.transform.scale(humb_midflap_mask, (PERIQUITO_WIDTH, PERIQUITO_WIDTH*1.3)),
                                                            pygame.transform.scale(humb_upflap_mask, (PERIQUITO_WIDTH, PERIQUITO_WIDTH*1.3)),
                                                            pygame.transform.scale(humb_midflap_mask, (PERIQUITO_WIDTH, PERIQUITO_WIDTH*1.3))]}

        self.impulso_snd = pygame.mixer.Sound(impulso_snd)
        self.crashing_snd = pygame.mixer.Sound(crashing_snd)
        self.falling_snd = pygame.mixer.Sound(falling_snd)
        self.point_snd =  pygame.mixer.Sound(point_snd)

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
        global pontuacao,cano_gap
        if (player.rect.right - canonormal.rect.left > 1 and player.rect.right - canonormal.rect.left < 10) and self.verificaponto ==0: 
            self.verificaponto = 1
        elif (player.rect.right - canonormal.rect.right > 1) and self.verificaponto ==1: 
            self.verificaponto = 0
            self.point_snd.play()
            cano_gap-= 1
            pontuacao +=1

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
 """