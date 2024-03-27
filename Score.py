from Const import (WIDTH, HEIGHT, CENTER_X, YELLOW, GRAY, BLACK, WHITE,
                   CENTER_Y, INSTRUCTIONS_BACKGROUNDCOLOR, GAME_OVER_BACKGROUND,WIN)
import pygame
import sys


def draw_button(text, position, size, is_hovered):
    font = pygame.font.SysFont("Arial", 32)
    text_surf = font.render(text, True, BLACK if is_hovered else WHITE)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(WIN, YELLOW if is_hovered else GRAY, button_rect)
    text_rect = text_surf.get_rect(center=button_rect.center)
    WIN.blit(text_surf, text_rect)
    return button_rect

def save_score(name, score, difficulty):
    with open("leaderboard.txt", "a") as file:
        file.write(f"{name} {score} {difficulty}\n")

def show_leaderboard():
    try:
        with open("leaderboard.txt", "r") as file:
            scores = [line.strip().split(' ', 2) for line in file]  # Split each line into name, score, and difficulty
            scores.sort(key=lambda x: int(x[1]), reverse=True)  # Sort scores in descending order
    except FileNotFoundError:
        scores = []

    # Buttons setup
    quit_button_position = (WIDTH // 2 - 100, (HEIGHT // 2) + 100, 200, 50)
    running = True
    while running:
        WIN.fill(INSTRUCTIONS_BACKGROUNDCOLOR)  # background color
        WIN.blit(GAME_OVER_BACKGROUND, (CENTER_X, CENTER_Y))
        font = pygame.font.SysFont("Arial", 24)
        title = font.render("Top 10 Players:", True, (255, 255, 255))
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

        for i, (name, score, difficulty) in enumerate(scores[:10], start=1):  # Display top 10 scores
            text = font.render(f"{i}. {name} - {score} - {difficulty}", True, (255, 255, 255))
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 30 + i * 30))

        mouse_pos = pygame.mouse.get_pos()
        quit_button_hovered = quit_button_position[0] < mouse_pos[0] < quit_button_position[0] + quit_button_position[
            2] and \
                              quit_button_position[1] < mouse_pos[1] < quit_button_position[1] + quit_button_position[3]

        draw_button("Quit?", quit_button_position[:2], quit_button_position[2:], quit_button_hovered)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if quit_button_hovered:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to exit leaderboard
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Click to exit leaderboard
                running = False