from Const import (WIDTH, HEIGHT, CENTER_X, YELLOW, GRAY, BLACK, WHITE,
                      CENTER_Y, INSTRUCTIONS_BACKGROUNDCOLOR, GAME_OVER_BACKGROUND,WIN)
import pygame


def get_player_name():
    font = pygame.font.SysFont("Arial", 32)
    current_name = []
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    WIN.fill(INSTRUCTIONS_BACKGROUNDCOLOR)  # background color
    WIN.blit(GAME_OVER_BACKGROUND, (CENTER_X, CENTER_Y))
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return ''.join(current_name)
                elif event.key == pygame.K_BACKSPACE:
                    current_name = current_name[:-1]
                else:
                    if len(current_name) < 10:  # Limit name length to 10 characters
                        current_name.append(event.unicode)

        text_surf = font.render("Enter Name: " + ''.join(current_name), True, (255, 255, 255))
        WIN.blit(text_surf, (input_box.x - 20, input_box.y + 5))
        pygame.display.update()