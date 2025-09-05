# Jogo da Cobrinha (Snake) em Python com Pygame
# Para executar, certifique-se de ter o Pygame instalado:
# pip install pygame

import pygame
import random

# Inicializa todos os módulos do Pygame
pygame.init()

# --- Definição de Cores (padrão RGB) ---
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)

# --- Configurações da Tela ---
largura_tela = 600
altura_tela = 400
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Jogo da Cobrinha com Python')

# --- Configurações do Jogo ---
clock = pygame.time.Clock()
tamanho_bloco = 10  # Tamanho de cada "quadrado" da cobrinha e da comida
velocidade_cobra = 15

# --- Fontes para Texto ---
fonte_estilo = pygame.font.SysFont("bahnschrift", 25)
fonte_score = pygame.font.SysFont("comicsansms", 35)


def exibir_score(score):
    """Função para exibir a pontuação na tela."""
    valor = fonte_score.render("Sua Pontuação: " + str(score), True, azul)
    tela.blit(valor, [0, 0])


def desenhar_cobra(tamanho_bloco, lista_cobra):
    """Função para desenhar a cobra na tela."""
    for x in lista_cobra:
        pygame.draw.rect(tela, verde, [x[0], x[1], tamanho_bloco, tamanho_bloco])


def exibir_mensagem(msg, cor):
    """Função para exibir uma mensagem centralizada na tela."""
    mensagem = fonte_estilo.render(msg, True, cor)
    # Pega o retângulo do texto e o centraliza na tela
    text_rect = mensagem.get_rect(center=(largura_tela / 2, altura_tela / 2))
    tela.blit(mensagem, text_rect)


def gameLoop():
    """Função principal que executa o loop do jogo."""
    game_over = False
    game_close = False

    # Posição inicial da cobra (centro da tela)
    x1 = largura_tela / 2
    y1 = altura_tela / 2

    # Variação da posição (inicialmente a cobra está parada)
    x1_change = 0
    y1_change = 0

    # A cobra é uma lista de segmentos. Começa com apenas a cabeça.
    lista_cobra = []
    comprimento_cobra = 1

    # Gera a posição inicial da comida
    comida_x = round(random.randrange(0, largura_tela - tamanho_bloco) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura_tela - tamanho_bloco) / 10.0) * 10.0

    # --- Loop Principal do Jogo ---
    while not game_over:

        # --- Tela de Fim de Jogo ---
        while game_close:
            tela.fill(preto)
            exibir_mensagem("Você Perdeu! Pressione C para Jogar Novamente ou Q para Sair", vermelho)
            exibir_score(comprimento_cobra - 1)
            pygame.display.update()

            # Verifica os eventos na tela de fim de jogo
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Se pressionar 'Q', sai do jogo
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:  # Se pressionar 'C', reinicia o jogo
                        gameLoop()
                if event.type == pygame.QUIT: # Permite fechar na janela
                    game_over = True
                    game_close = False


        # --- Processamento de Eventos (Teclado) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -tamanho_bloco
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = tamanho_bloco
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -tamanho_bloco
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = tamanho_bloco
                    x1_change = 0

        # --- Lógica de Colisão com as Bordas ---
        if x1 >= largura_tela or x1 < 0 or y1 >= altura_tela or y1 < 0:
            game_close = True

        # Atualiza a posição da cabeça da cobra
        x1 += x1_change
        y1 += y1_change

        # Preenche o fundo da tela
        tela.fill(preto)

        # Desenha a comida
        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])

        # Adiciona a nova posição da cabeça à lista da cobra
        cabeca_cobra = []
        cabeca_cobra.append(x1)
        cabeca_cobra.append(y1)
        lista_cobra.append(cabeca_cobra)

        # Remove o último segmento da cobra para dar a ilusão de movimento
        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        # --- Lógica de Colisão com o Próprio Corpo ---
        # Verifica se a cabeça colidiu com qualquer outra parte do corpo
        for x in lista_cobra[:-1]:
            if x == cabeca_cobra:
                game_close = True

        # Desenha a cobra na tela
        desenhar_cobra(tamanho_bloco, lista_cobra)
        # Exibe a pontuação
        exibir_score(comprimento_cobra - 1)

        # Atualiza a tela para mostrar o que foi desenhado
        pygame.display.update()

        # --- Lógica de Colisão com a Comida ---
        if x1 == comida_x and y1 == comida_y:
            # Gera uma nova posição para a comida que não esteja sobre a cobra
            while True:
                comida_x = round(random.randrange(0, largura_tela - tamanho_bloco) / 10.0) * 10.0
                comida_y = round(random.randrange(0, altura_tela - tamanho_bloco) / 10.0) * 10.0
                posicao_comida = [comida_x, comida_y]
                if posicao_comida not in lista_cobra:
                    break
            
            # Aumenta o comprimento da cobra (não removemos o último segmento)
            comprimento_cobra += 1

        # Define a taxa de atualização da tela (FPS)
        clock.tick(velocidade_cobra)

    # Finaliza o Pygame e fecha o programa
    pygame.quit()
    quit()


# Inicia o jogo
gameLoop()

