import pygame
import sys
import random
import time
from db import get_quetion
from model import check_letter, check_letter_in_list, remote_letter


def start_Field_of_Dreams():
    # Инициализация Pygame
    pygame.init()

    # Размеры экрана
    screen_width = 800
    screen_height = 600

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    font_bold = pygame.font.Font("fonts/press.ttf", 18)
    font_bold_little = pygame.font.Font("fonts/press.ttf", 8)

    # Создание экрана
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Field of Wonders")

    # Размеры и положение игровой области
    game_area_width = 640  # Ширина сетки 16 * 40
    game_area_height = 200
    game_area_x = 80  # Уменьшено смещение по X для центрирования
    game_area_y = 40

    edit_txt = "Welcome to the Field \nof Wonders!"
    gg_txt = "Thank you"
    #попытка пользователя
    attempt = 5


    # фотографии 
    backgraund = pygame.image.load('image/pole_chudes.jpg')
    backgraund = pygame.transform.scale(backgraund, (800, 600))

    quetion_back = pygame.image.load('image/quetions-removebg-preview.png')
    quetion_back = pygame.transform.scale(quetion_back, (800, 100))
    quetion_back = pygame.transform.flip(quetion_back, True, False)


    message_back = pygame.image.load('image/message.png')
    message_back = pygame.transform.scale(message_back, (230, 150))
    message_back = pygame.transform.rotate(message_back, 180)
    message_gg_back = pygame.transform.scale(message_back, (200, 100))
    message_gg_back = pygame.transform.flip(message_gg_back, True, False)
    

    # Размеры клетки
    cell_width = game_area_width // 16  # Делим на 16 для 16 клеток в строке
    cell_height = game_area_height // 5 # Делим на 5 для 5 клеток в столбце

    
    # Генерация случайного числа от 1 до 20
    randomNum = random.randint(1, 20)
    quetion = get_quetion(randomNum)
    length = len(quetion[2])
    word = quetion[2]

    quetion_table = font_bold_little.render(quetion[1], True, BLACK)
    quetion_rect = quetion_table.get_rect()
    quetion_rect.center = (400, 50)

    even_and_odd = 0
    if length % 2 == 1:
        even_and_odd = 1

    # Функция для создания сетки клеток
    def create_grid():
        grid = []
        for i in range(16):  # Изменено на 16
            grid.append([])
            for j in range(5):
                # Используем словарь для хранения информации о клетке
                cell_info = {
                    "rect_color": BLUE if j == 2 and (i >= (16 - length) // 2 and i < 16 - (((16 - length) // 2)) - even_and_odd) else WHITE,
                    "x": game_area_x + i * cell_width,
                    "y": game_area_y + j * cell_height,
                    "width": cell_width,
                    "height": cell_height,
                    "border_color": BLACK,
                    "text": ""
                }
                grid[i].append(cell_info)  # Исправлено: добавляем клетку во внутренний список
        return grid
    
    # Создание сетки клеток
    grid = create_grid()

    cnt_word = (16 - length) // 2  # Изменено на 16

    list_letter = []
    # Основной игровой цикл
    running = True
    quit_game = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z and cnt_word <= length+(16 - length) // 2:
                    # Обновляем текст в синем блоке
                    letter = chr(event.key).lower()
                    list_gg_txt = [f"Maybe letter {letter.upper()}?", f"Next letter is {letter.upper()}.", f"I choose letter {letter.upper()}.", f"Let's check if \nthere is letter {letter.upper()}."]
                    gg_txt = random.choice(list_gg_txt)
                    if check_letter_in_list(letter, list_letter):
                        edit_txt = f"This letter \nhas already \nbeen selected \npreviously. Please \nchoose another one."
                    else:
                        list_letter.append(letter)
                        if check_letter(letter, word):
                            edit_txt = f"Let's reveal the \nletter {letter.upper()}."
                            i = cnt_word
                            for let in quetion[2]:
                                if letter == let:
                                    grid[i][2]["text"] = letter.upper()
                                i += 1
                            word = remote_letter(letter, word)
                        elif attempt == 2:
                            attempt -= 1
                            edit_txt = "Sorry, but that \nletter is not in the \nword. You have one \nattempt left, use \nit wisely."
                        elif attempt > 2:
                            attempt -= 1
                            edit_txt = f"You didn't guess, \nyou have only {attempt} \nattempts left."
                        elif attempt == 1:
                            edit_txt = f"You lost, the word was \n{word.upper()}."
                            quit_game = 1
                    if not word:
                        edit_txt = "Congratulations, \nyou guessed \nthe word correctly!!"
                        quit_game = 2
                        

        # Заливка фона
        screen.fill(WHITE)
        screen.blit(backgraund, (0, 0))
        
        # Рисуем рамку игровой области
        pygame.draw.rect(screen, BLACK, (game_area_x, game_area_y, game_area_width, game_area_height), 2)
        
        # Рисуем заштрихованные клетки и текст
        for i in range(16):  # Изменено на 16
            for j in range(5):
                pygame.draw.rect(screen, grid[i][j]["rect_color"], (grid[i][j]["x"] + 1, grid[i][j]["y"] + 1, grid[i][j]["width"] - 2, grid[i][j]["height"] - 2), 0)
                pygame.draw.rect(screen, grid[i][j]["border_color"], (grid[i][j]["x"], grid[i][j]["y"], grid[i][j]["width"], grid[i][j]["height"]), 1)
                # Рисуем текст
                
                text_surface = font_bold.render(grid[i][j]["text"], True, WHITE)
                text_rect = text_surface.get_rect(center=(grid[i][j]["x"] + grid[i][j]["width"] // 2, grid[i][j]["y"] + grid[i][j]["height"] // 2))
                screen.blit(text_surface, text_rect)

        screen.blit(quetion_back, (0, 10))
        screen.blit(quetion_table, quetion_rect)

        screen.blit(message_gg_back, (180, 370))
        screen.blit(message_back, (400, 360))

        # ответы героя
        lines_gg = gg_txt.split('\n')
        posi_y = 420
        for line in lines_gg:
            gg_txt_block = font_bold_little.render(line, True, BLACK)
            screen.blit(gg_txt_block, (200, posi_y))
            posi_y +=15

        # ответы ведущего
        lines = edit_txt.split('\n')
        pos_y = 420
        for line in lines:
            edit_txt_block = font_bold_little.render(line, True, BLACK)
            screen.blit(edit_txt_block, (430, pos_y))
            pos_y +=15
        
        
        # Обновление экрана
        pygame.display.flip()
        if quit_game == 1:
            time.sleep(3)
            return False
        elif quit_game == 2:
            time.sleep(3)
            return True
    # Выход из Pygame
    pygame.quit()
    sys.exit()
