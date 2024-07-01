import pygame
import matplotlib.backends.backend_agg as agg
import pylab
import matplotlib

COR_BRANCA = (255, 255, 255)
COR_PRETA = (0, 0, 0)

LARGURA_TELA = 1200
ALTURA_TELA = 600

clock = pygame.time.Clock()
FPS = 10
window_size = (LARGURA_TELA, ALTURA_TELA)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tech Chalenge - Problema da mochila")

screen.fill(COR_BRANCA)

def tick_clock():
    pygame.display.flip()

    clock.tick(FPS)

def quit_pygame():
    pygame.quit()

#### DRAW FUNCTIONS####

def draw_plot(x, y, x_label='Generation', y_label='Fitness'):
    fig = pylab.figure(figsize=[10, 6],  # Inches
                       dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                       )
    ax = fig.gca()
    # ax.plot(random_integers[:i])
    ax.plot(x, y)

    # Adicionando título ao gráfico
    ax.set_title("Problema da mochila")

    # Adicionando labels aos eixos
    ax.set_xlabel("Geração")
    ax.set_ylabel("Valor da mochila")

    # Exibindo a grade de fundo
    ax.grid(True)

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    # window = pygame.display.set_mode((600, 400), DOUBLEBUF)
    # screen = pygame.display.get_surface()

    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 0))

    matplotlib.pyplot.close()

def draw_text(screen, text, x_position, y_position, color=(0, 0, 0), font_size=30, font='Arial'):
    # Initialize Pygame font
    pygame.font.init()

    # limpa a tela para evitar sobreposição
    screen.fill(COR_BRANCA, (LARGURA_TELA - 200, 0, 200, ALTURA_TELA))

    # Set the font and size
    font = pygame.font.SysFont(font, font_size)

    # Render the text
    text_surface = font.render(text, True, color)

    # Get the rectangle containing the text surface
    text_rect = text_surface.get_rect()

    # Set the position of the text
    text_rect.topleft = (x_position, y_position)

    # Blit the text onto the screen
    screen.blit(text_surface, text_rect)


pygame.init()