import pygame
import random

# Константы для цветов и размеров клеток
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
WIDTH = 29
HEIGHT = 22
MARGIN = 2

# Создание сетки для лабиринта
def create_grid():
    grid = []
    for row in range(25):
        grid.append([])
        for column in range(25):
            grid[row].append(1)  # 1 - стена, 0 - проход
    return grid

# Функция для создания случайного пути в лабиринте
def create_maze(grid, row, column):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    for dr, dc in directions:
        new_row = row + 2 * dr
        new_col = column + 2 * dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] == 1:
            grid[row + dr][column + dc] = 0
            grid[new_row][new_col] = 0
            create_maze(grid, new_row, new_col)

# Функция для проверки, есть ли черная стена в соседних клетках
def has_black_neighbor(grid, row, col):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] == 1:
            return True
    return False

grid = create_grid()
create_maze(grid, 1, 1)

start_row = random.randint(1, len(grid) - 2)
start_col = 0
while not has_black_neighbor(grid, start_row, start_col):
    start_row = random.randint(1, len(grid) - 2)
    start_col = 0

end_row = random.randint(1, len(grid) - 2)
end_col = len(grid[0]) - 1
while not has_black_neighbor(grid, end_row, end_col):
    end_row = random.randint(1, len(grid) - 2)
    end_col = len(grid[0]) - 1

grid[start_row][start_col] = 2  # 2 - старт
grid[end_row][end_col] = 3  # 3 - конец

available_cells = []
for row in range(len(grid)):
    for col in range(len(grid[row])):
        if grid[row][col] == 0 and (row != start_row or col != start_col):
            available_cells.append((row, col))

coins = []
for _ in range(15):
    coin_row, coin_col = random.choice(available_cells)
    coins.append((coin_row, coin_col))

game_state = "playing"
player_pos = [start_row, start_col]
timer = 3600
show_notification = False


def start_labyrinth():
    global grid, start_row, start_col, end_row, end_col, coins, game_state, player_pos, timer, show_notification, player_pos, show_notification
    # Инициализация Pygame
    pygame.init()

    # Установка размеров экрана
    WINDOW_SIZE = [(WIDTH + MARGIN) * 25 + MARGIN, (HEIGHT + MARGIN) * 25 + MARGIN]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Установка заголовка окна
    pygame.display.set_caption("Random Maze with Start, End Points, and Gold Coins")

    # Основной цикл программы
    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state == "menu":
                mouse_pos = pygame.mouse.get_pos()
                if (WINDOW_SIZE[0] - 100) / 2 <= mouse_pos[0] <= (WINDOW_SIZE[0] - 100) / 2 + 100 and \
                        (WINDOW_SIZE[1] - 50) / 2 + 60 <= mouse_pos[1] <= (WINDOW_SIZE[1] - 50) / 2 + 100:
                    # Клик произошел на кнопке "Выйти"
                    return timer
                else:
                    game_state = "playing"
                    timer = 3600  # Начинаем таймер при нажатии на кнопку "Старт"
            elif event.type == pygame.KEYDOWN and game_state == "playing" and not show_notification:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and player_pos[0] > 0 and grid[player_pos[0] - 1][player_pos[1]] != 1:
                    player_pos[0] -= 1  # Вверх
                elif event.key == pygame.K_s and player_pos[0] < len(grid) - 1 and grid[player_pos[0] + 1][player_pos[1]] != 1:
                    player_pos[0] += 1  # Вниз
                elif event.key == pygame.K_a and player_pos[1] > 0 and grid[player_pos[0]][player_pos[1] - 1] != 1:
                    player_pos[1] -= 1  # Влево
                elif event.key == pygame.K_d and player_pos[1] < len(grid[0]) - 1 and grid[player_pos[0]][player_pos[1] + 1] != 1:
                    player_pos[1] += 1  # Вправо

        # Проверка сбора монеток
        coins_to_remove = []
        for coin_row, coin_col in coins:
            if player_pos[0] == coin_row and player_pos[1] == coin_col:
                coins_to_remove.append((coin_row, coin_col))
                show_notification = True  # Устанавливаем состояние показа уведомления
        for coin_row, coin_col in coins_to_remove:
            coins.remove((coin_row, coin_col))

        # Проверка достижения финиша
        if player_pos[0] == end_row and player_pos[1] == end_col:
            game_state = "finished"

        # Обновление таймера только в режиме игры
        if game_state == "playing":
            if timer > 0 and not show_notification:
                timer -= 1
            # Проверка на проигрыш по времени
            if timer <= 0:
                game_state = "lost"


        # Отрисовка лабиринта, персонажа и золотых монеток
        screen.fill(BLACK)
        for row in range(len(grid)):
            for column in range(len(grid[row])):
                if grid[row][column] == 1:
                    color = WHITE
                elif grid[row][column] == 2:
                    color = RED
                elif grid[row][column] == 3:
                    color = GREEN
                else:
                    color = BLACK
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN,
                                                (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
        for coin_row, coin_col in coins:
            pygame.draw.circle(screen, GOLD, ((MARGIN + WIDTH) * coin_col + MARGIN + WIDTH // 2,
                                            (MARGIN + HEIGHT) * coin_row + MARGIN + HEIGHT // 2),
                            min(WIDTH, HEIGHT) // 4)
        pygame.draw.circle(screen, RED, ((MARGIN + WIDTH) * player_pos[1] + MARGIN + WIDTH // 2, 
                                        (MARGIN + HEIGHT) * player_pos[0] + MARGIN + HEIGHT // 2), 
                        min(WIDTH, HEIGHT) // 2)
        # Отрисовка таймера
        font = pygame.font.Font(None, 36)
        text = font.render("Timer: " + str(timer // 60) + ":" + str(timer % 60).zfill(2), True, RED)
        screen.blit(text, (10, 10))
        # Обновление таймера
        if timer > 0 and not show_notification:
            timer -= 1

        # Обработка уведомления о сборе монетки
        if show_notification:
            pygame.draw.rect(screen, BLACK, (100, 200, WINDOW_SIZE[0] - 200, 200))  # Фон уведомления
            font = pygame.font.Font(None, 24)
            text = font.render("Вы получили монетку", True, WHITE)
            screen.blit(text, (150, 250))  # Текст уведомления

            # Рисование красного квадрата для закрытия уведомления
            pygame.draw.rect(screen, RED, (WINDOW_SIZE[0] - 150, 210, 30, 30))

            # Добавление текста "X" на красный квадрат
            font_x = pygame.font.Font(None, 24)
            text_x = font_x.render("X", True, BLACK)
            screen.blit(text_x, (WINDOW_SIZE[0] - 140, 215))

        # Обработка события закрытия уведомления
        if show_notification:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if WINDOW_SIZE[0] - 150 <= mouse_pos[0] <= WINDOW_SIZE[0] - 10 and 210 <= mouse_pos[1] <= 240:
                    show_notification = False  # Закрываем уведомление

        # Обработка события клика на кнопку "Вернуться в меню"
        if game_state == "finished":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (WINDOW_SIZE[0] - 200) / 2 <= mouse_pos[0] <= (WINDOW_SIZE[0] - 200) / 2 + 200 and \
                (WINDOW_SIZE[1] + 100) / 2 <= mouse_pos[1] <= (WINDOW_SIZE[1] + 100) / 2 + 50:
                    game_state = "menu"
                    player_pos = [start_row, start_col]
                    timer = 3600
                    show_notification = False

        # Обновление экрана
        pygame.display.flip()

        # Задержка для обновления экрана
        clock.tick(60)

    # Выход из Pygame
    pygame.quit()
    return grid, timer

