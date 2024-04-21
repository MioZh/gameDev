import pygame, time
from game.player import *
from game.enemies import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

def start_pacman():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PACMAN")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 40)
    game_over = False
    win = False
    score = 0
    
    player = Player(32,128,"game/images_pacman/player.png")
    # Create the blocks that will set the paths where the player can go
    horizontal_blocks = pygame.sprite.Group()
    vertical_blocks = pygame.sprite.Group()
    dots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    for i,row in enumerate(environment()):
        for j,item in enumerate(row):
            if item == 1:
                horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
            elif item == 2:
                vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
    # Add the dots inside the game
    for i,row in enumerate(environment()):
        for j,item in enumerate(row):
            if item != 0:
                dot = Ellipse(j*32+12,i*32+12,WHITE,8,8)
                dots.add(dot)

    enemies.add(Slime(288,96,0,2))
    enemies.add(Slime(288,320,0,-2))
    enemies.add(Slime(160,64,2,0))
    enemies.add(Slime(448,64,-2,0))
    enemies.add(Slime(640,448,2,0))
    
    game_over_sound = pygame.mixer.Sound("game/audio_pacman/game_over_sound.mp3")
    win_sound = pygame.mixer.Sound("game/audio_pacman/win_sound.mp3")

    # Win Screen
    wintext = font.render("Congratulations! You finished the game!", True, BLACK)
    wintextRect = wintext.get_rect()
    wintextRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_UP:
                    player.move_up()
                elif event.key == pygame.K_DOWN:
                    player.move_down()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    player.stop_move_left()
                elif event.key == pygame.K_UP:
                    player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    player.stop_move_down()
        
        player.update(horizontal_blocks, vertical_blocks)
        block_hit_list = pygame.sprite.spritecollide(player, dots, True)
        if block_hit_list:
            score += 1

        if len(dots) == 0:
            win = True
            game_over = True
        
        block_hit_list = pygame.sprite.spritecollide(player, enemies, True)
        if block_hit_list:
            game_over_sound.play()
            return False
        
        game_over = player.game_over
        enemies.update(horizontal_blocks, vertical_blocks)
        
        screen.fill(BLACK)
        horizontal_blocks.draw(screen)
        vertical_blocks.draw(screen)
        draw_environment(screen)
        dots.draw(screen)
        enemies.draw(screen)
        screen.blit(player.image, player.rect)
        text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(text, [20, 20])

        if win:
            return True
            
        pygame.display.flip()
        clock.tick(30)
        
    time.sleep(2)
    pygame.quit()
