import pygame
import random

# Inicialização
pygame.init()

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configurações da tela
WIDTH, HEIGHT = 300, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Constantes
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# Peças
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],
    [[1, 1, 0],
     [1, 1, 0]],
    [[1, 1, 1, 1]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
    [[1, 1, 1],
     [1, 0, 0]],
    [[1, 1],
     [1, 1]]
]

SCORE = 0

# Lista de cores aleatórias
COLORS = [(0, 0, 255),  # Azul
          (0, 255, 0),  # Verde
          (255, 0, 0),  # Vermelho
          (255, 182, 193),  # Rosa
          (255, 165, 0)]  # Laranja
random.shuffle(COLORS)  # Lista de cores aleatoria

def draw_block(x, y, color=WHITE):
    pygame.draw.rect(SCREEN, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(SCREEN, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            draw_block(x, y, BLACK)

def draw_shape(shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col] == 1:
                draw_block(x + col, y + row, color)

def can_move(shape, x, y, grid):
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col] == 1:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col] != BLACK:
                    return False
    return True

def rotate_shape(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0])-1, -1, -1)]

def check_complete_lines(grid):
    complete_lines = []
    for y in range(len(grid)):
        if all(grid[y][x] != BLACK for x in range(len(grid[y]))):
            complete_lines.append(y)
    return complete_lines

def draw_score():
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {SCORE}", True, WHITE)
    SCREEN.blit(text, (10, 10))

def main():
    global SCORE, COLORS

    running = True
    current_x, current_y = 5, 0
    current_shape = SHAPES[random.randint(0, len(SHAPES) - 1)]
    current_color = COLORS.pop(0)  # Pegar a primeira cor da lista embaralhada
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5

    while running:
        dt = clock.tick(60) / 1000.0
        fall_time += dt

        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and can_move(current_shape, current_x - 1, current_y, grid):
                    current_x -= 1
                elif event.key == pygame.K_RIGHT and can_move(current_shape, current_x + 1, current_y, grid):
                    current_x += 1
                elif event.key == pygame.K_DOWN and can_move(current_shape, current_x, current_y + 1, grid):
                    current_y += 1
                elif event.key == pygame.K_UP:
                    current_shape = rotate_shape(current_shape)

        if fall_time >= fall_speed:
            if can_move(current_shape, current_x, current_y + 1, grid):
                current_y += 1
            else:
                # Fixar peça no grid
                for row in range(len(current_shape)):
                    for col in range(len(current_shape[0])):
                        if current_shape[row][col] == 1:
                            grid[current_y + row][current_x + col] = current_color

                # Verificar e remover linhas completas
                complete_lines = check_complete_lines(grid)
                if complete_lines:
                    SCORE += len(complete_lines) * 100
                    for y in complete_lines:
                        grid.pop(y)
                        grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])

                current_x, current_y = 5, 0
                current_shape = SHAPES[random.randint(0, len(SHAPES) - 1)]

                if not COLORS:  # Se a lista de cores estiver vazia, embaralhe-a novamente
                    COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 182, 193), (255, 165, 0)]
                    random.shuffle(COLORS)

                current_color = COLORS.pop(0)  # Pegar a próxima cor da lista

            fall_time = 0

        draw_grid()
        for y, row in enumerate(grid):
            for x, color in enumerate(row):
                if color != BLACK:
                    draw_block(x, y, color)
        draw_shape(current_shape, current_x, current_y, current_color)
        draw_score()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()