import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
# Цвета
WHITE = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Анимация ходьбы")

# Загрузка изображений для анимации ходьбы
walk_images_left = [pygame.image.load('player/left_a.png'),
                    pygame.image.load('player/left_b.png'),
                    pygame.image.load('player/left_c.png')]

walk_images_right = [pygame.image.load('player/right_a.png'),
                     pygame.image.load('player/right_b.png'),
                     pygame.image.load('player/right_c.png')]

# Размеры изображений (для центрирования)
img_width, img_height = walk_images_left[0].get_rect().size

# Начальное положение персонажа
x, y = WIDTH // 2 - img_width // 2, HEIGHT // 2 - img_height // 2

# Индекс текущего кадра анимации
current_frame = 0

# Скорость анимации (чем меньше, тем быстрее)
animation_speed = 50
current_alpha = 1
# Направление движения (по умолчанию - вправо)
direction = 'right'

# Функция плавного перехода между изображениями
def smooth_transition(image1, image2, alpha):
    # Масштабируем изображения до одного размера
    width = min(image1.get_width(), image2.get_width())
    height = min(image1.get_height(), image2.get_height())
    image1 = pygame.transform.scale(image1, (width, height))
    image2 = pygame.transform.scale(image2, (width, height))

    # Получаем массивы пикселей для обоих изображений
    pixels1 = pygame.surfarray.array3d(image1)
    pixels2 = pygame.surfarray.array3d(image2)

    # Вычисляем новый массив пикселей на основе плавного перехода
    new_pixels = (pixels1 * alpha + pixels2 * (1 - alpha)).astype(int)

    # Создаем новое изображение на основе нового массива пикселей
    new_image = pygame.surfarray.make_surface(new_pixels)

    return new_image


# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Проверяем достижение определенной координаты
    if x == 400:  # Пример: когда персонаж достигает x=400, меняем направление
        direction = 'left'
    elif x == 200:
        direction = 'right'

    # Определяем текущий список изображений в зависимости от направления движения
    current_images = walk_images_right if direction == 'right' else walk_images_left

    # Обновляем текущий кадр анимации
    current_frame = (current_frame + 1) % len(current_images)

    # Плавное изменение прозрачности текущего кадра анимации
    current_alpha -= 0.01
    if current_alpha < 0:
        current_alpha = 1

    # Применяем плавное изменение цветовых каналов к текущему кадру анимации
    current_image = smooth_transition(current_images[current_frame], current_images[(current_frame + 1) % len(current_images)], current_alpha)

    # Отображение фона и текущего кадра анимации персонажа
    screen.fill(WHITE)
    screen.blit(current_image, (x, y))  # x и y - координаты персонажа на экране

    # Обновление экрана
    pygame.display.flip()

    # Задержка для плавности анимации
    pygame.time.delay(animation_speed)

    # Изменение координаты персонажа для примера движения
    if direction == 'right':
        x += 1
    else:
        x -= 1

# Завершение работы Pygame
pygame.quit()
sys.exit()
