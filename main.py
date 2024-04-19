import pygame
from register import register
from log import log

pygame.init()

# Setting window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Register and Login")

# Define fonts
font = pygame.font.Font("fonts/press.ttf", 18)
font_bold = pygame.font.Font("fonts/press.ttf", 18)

background_image = pygame.image.load("image/reglog_backgraund.jpg")
background_image = pygame.transform.scale(background_image, (800, 600))
background_rect = background_image.get_rect()

original_image = pygame.image.load('pict/but_l.png')
# Resize image
button_image = pygame.transform.scale(original_image, (180, 80))

# Rendering text images
register_text = font_bold.render("Sign in", True, (255, 255, 255))  # White color
register_rect = register_text.get_rect()
register_rect.bottomleft = (500, 200)  # Positioning at the center horizontally

login_text = font_bold.render("Log in", True, (255, 255, 255))  # White color
login_rect = login_text.get_rect()
login_rect.bottomleft = (500, 280)  # Positioning at the bottom left corner

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 475 <= event.pos[0] <= 645 and 140 <= event.pos[1] <= 210:
                register()
            if 475 <= event.pos[0] <= 645 and 225 <= event.pos[1] <= 290:
                log()
            
    screen.blit(background_image, background_rect)
    
    # Blitting button image onto the screen
    screen.blit(button_image, (register_rect.x - 30, register_rect.y - 30))  # Adjust position to center the button
    screen.blit(button_image, (login_rect.x - 30, login_rect.y - 30))  # Adjust position to center the button
    
    # Blitting text images onto the screen
    screen.blit(register_text, register_rect)
    screen.blit(login_text, login_rect)

    pygame.display.flip()

pygame.quit()
