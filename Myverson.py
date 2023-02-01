# Biblioteca PyGame
import pygame
# Biblioteca para geração de números pseudoaleatórios
import random
# Módulo da biblioteca PyGame que permite o acesso às teclas utilizadas
from pygame.locals import *

# Classe que representar o jogador
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        
        self.surf = pygame.image.load('imgs\protats.gif') #Define a imagem que representa o player
        self.rect = self.surf.get_rect()

    # Determina ação de movimento conforme teclas pressionadas
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        # Mantém o jogador nos limites da tela do jogo
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

#variaveis globais
score_value = 0 
dificuldade = 0

# Classe que representa os inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self): 
        super(Enemy, self).__init__()
        
        self.surf = pygame.image.load('imgs/enemyts.png')

        self.rect = self.surf.get_rect( #Coloca na extrema direita (entre 820 e 900) e 
        #sorteia sua posição em relacao à coordenada y (entre 0 e 600)
        
            center=(random.randint(820, 900), random.randint(0, 600))
        )

        global dificuldade

        #Aumentando a velocidade conforme a quantidade de pontos
        if score_value >= 50 and score_value < 100:
            dificuldade = 1
        if score_value >= 100 and score_value < 200:
            dificuldade = 2
        if score_value >= 200 and score_value < 400:
            dificuldade = 3
        if score_value >= 400:
            dificuldade = 4

        self.speed = random.uniform(1 + dificuldade, 4 + dificuldade) #Sorteia sua velocidade, e aumenta com a pontuação

    #Função que atualiza a posiçao do inimigo em função da sua velocidade e termina 
    #com ele quando ele atinge o limite esquerdo da tela (x < 0)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill() 

            global score_value #Define uma variavel global para que eu possa usar ela em qualquer lugar do codigo
            score_value += 1 #incrementador de pontos do score
            barulho_colizao.play() #som de aviso do score sendo incrementado

def showScore(): #Função pra escrever o score
    score = font.render("SCORE: " + str(score_value), False, (40,40,40))
    ret_texto1 = score.get_rect() #Coloca o conteudo em uma caixa
    ret_texto1.center = (400,50) # Alinha com o centro
    screen.blit(score,(ret_texto1)) #Coloca na tela

# Inicializa pygame
pygame.init()

# Cria a tela com resolução 800x600px
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Raimbow CAT')

barulho_colizao = pygame.mixer.Sound('music/smw_coin.wav') #Colocar o som do score
musica = pygame.mixer.music.load('music/musc.wav') #Colocar a musiquinha de fundo
pygame.mixer.music.play(-1) #Fazer a musiquinha de fundo repetir

font = pygame.font.SysFont('cambria', 30, True, False) #Define uma fonte do meu gosto

# Cria um evento para adição de inimigos
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 200) #Define um intervelao para a criação de cada inimigo (milisegundos)
 
# Cria o jogador (nosso retangulo)
player = Player()

# Define o plano de fundo como a imagem
background = pygame.image.load('imgs/backgroundts.jpg').convert()

enemies = pygame.sprite.Group() #Cria o grupo de inimigos
all_sprites = pygame.sprite.Group() #Cria o grupo de todos os Sprites
all_sprites.add(player) #Adicionar o player no grupo de todos os Sprites

running = True #Flag para controle do jogo

while running:

    pygame.time.delay(10)

    #Laco para verificação do evento que ocorreu
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q: #Verifica se a tecla Q foi pressionada
                running = False
        elif event.type == QUIT: #Verifica se a janela foi fechada
            running = False
        elif(event.type == ADDENEMY): #Verifica se é o evento de criar um inimigo
            new_enemy = Enemy() #Cria um novo inimigo
            enemies.add(new_enemy) #Adiciona o inimigo no grupo de inimigos
            all_sprites.add(new_enemy) #Adiciona o inimigo no grupo de todos os Sprites
    
    screen.blit(background, (0, 0)) #Atualiza a exibição do plano de fundo do jogo 
    #(neste caso não surte efeito)

    pressed_keys = pygame.key.get_pressed() #Captura as teclas pressionadas
    player.update(pressed_keys) #Atualiza a posição do player conforme teclas usadas
    enemies.update() #Atualiza posição dos inimigos

    showScore() #chama a função do score

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect) #Atualiza a exibição de todos os Sprites

    if pygame.sprite.spritecollideany(player, enemies): #Verifica se ocorreu a colisão do player com um dos inimigos        
                     
        #Mostrar que o jogo acabou
        textfim = font.render('GAME OVER! pressione Q para sair', False, (255,255,0))
        ret_texto2 = textfim.get_rect() #Coloca o conteudo em uma caixa
        #Mostrar o score final
        scorefim = font.render("SCORE FINAL: " + str(score_value), False, (255,255,0))
        ret_texto3 = scorefim.get_rect() #Coloca o conteudo em uma caixa

        morreu = True #trava para o jogo não sair de uma vez
        while morreu:

            screen.fill((75,0,130)) #Mudar a cor da tela
            for event in pygame.event.get(): #Laco para verificação do evento que ocorreu
                if event.type == QUIT: #Verifica se a janela foi fechada
                    pygame.quit()
                    exit() #fecha o jogo
                
                if event.type == KEYDOWN:
                    if event.key == K_q: #Verifica se a tecla Q foi pressionada
                        pygame.quit()
                        exit() #fecha o jogo
            
            ret_texto2.center = (400,270) #Coloca no centro
            screen.blit(textfim,(ret_texto2)) #Coloca na tela o game over

            ret_texto3.center = (400,320) #Coloca no centro
            screen.blit(scorefim,(ret_texto3)) #Coloca na tela o score final

            pygame.display.update()

    pygame.display.flip() #Atualiza a projeção do jogo

    