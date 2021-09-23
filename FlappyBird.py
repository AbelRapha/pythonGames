import pygame
import os
import random

#Configurações de Layout

#Largura da tela
largura_tela = 5000
#Altura da Tela
altura_tela = 800
#Adicionando as imagens
imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
imagem_background = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
imagens_passaros = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

#definindo as fontes

pygame.font.init()
fonte_dos_pontos = pygame.font.SysFont('arial', 50)


class Passaro:
    imagens = imagens_passaros
    #animacoes da rotacao
    rotacao_max = 25
    velocidade_rotacao = 20
    tempo_animacao = 5

    def __init__(self, x, y) -> None:
        """
        velocidade: Velocidade vertical (Sobe e desce)
        contagem_imagem: define qual imagem da minha lista de imagens do passaro estou usando em determinado momento
        """
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contage_imagem = 0
        self.imagem = self.imagens[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #Calcular o deslocamento
        self.tempo +=1
        deslocamento = 1.5 *(self.tempo**2) + self.velocidade * self.tempo
        #restringir deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento
        # angulo do passaro     
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_max:
                self.angulo = self.rotacao_max
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_rotacao
    def desenhar(self, tela):
        #Definir qual imagem do passaro vai usar
        self.contage_imagem += 1

        if self.contage_imagem < self.tempo_animacao:
            self.imagem = self.imagens[0]
        elif self.contage_imagem < self.tempo_animacao*2:
            self.imagem = self.imagens[1]
        elif self.contage_imagem < self.tempo_animacao*3:
            self.imagem = self.imagens[2]
        elif self.contage_imagem < self.tempo_animacao*4:
            self.imagem = self.imagens[1]
        elif self.contage_imagem >= self.tempo_animacao*4 +1:
            self.imagem = self.imagens[0]
            self.contage_imagem = 0
        #Se o passaro tiver caindo o passaro nao bate a asa
        if self.angulo == -80:
            self.imagem = self.imagens[1]
            self.contage_imagem = self.tempo_animacao*2
        #Desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posicao_centro_imagem = self.imagem.get_rect(topleft=(self.x,self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=posicao_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def obter_mascara(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self,x):
        self.x = x
        self.altura = 0
        self.posicao_topo = 0
        self.posicao_base = 0
        self.cano_topo = pygame.transform.flip(imagem_cano, False, True)
        self.cano_base = imagem_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50,450)
        self.posicao_base = self.altura - self.cano_topo.get_height()
        self.posicao_base = self.altura + self.distancia

    def mover(self):
        self.x = self.velocidade

    def desenhar(self,tela):
        tela.blit(self.cano_topo, (self.x,self.posicao_topo))
        tela.blit(self.cano_base, (self.x, self.posicao_base))
    
    def colidir(self, passaro):
        passaro_mascara = passaro.get_mask()
        topo_mascara = pygame.mask.from_surface(self.cano_topo)
        base_mascara = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.posicao_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.posicao_base - round(passaro.y))

        topo_ponto = passaro_mascara.overlap(topo_mascara,distancia_topo)
        base_ponto = passaro_mascara.overlap(base_mascara,distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    velocidade = 5
    largura = imagem_chao.get_width()
    imagem = imagem_chao

    def __init__(self,y):
        self.y = y
        self.x0 = 0
        self.x1 = self.largura

    def mover(self):
        self.x1 -= self.velocidade #Movimentando no sentido negativo do eixo x
        self.x0 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.largura
        if self.x0 + self.largura < 0:
            self.x0 = self.x0 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(imagem_background, (0,0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    
    texto = fonte_dos_pontos.reader(f'Pontuação: {pontos}', 1, (255,255,255))
    tela.blit(texto, (largura_tela -10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [Passaro(230,350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pontos = 0
    relogio = pygame.time.Clock()

    while True:
        relogio.tick(30) #fps
        #Interacao do usuario
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                break
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                for passaro in passaros:
                    passaro.pular()
        #Move os objetos
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano_passou and passaro.x > cano.x:
                    cano_passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))        
        for cano in remover_canos:
            cano.remove(cano)

        for i, passaro  in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()