from Const import *
from main import WIN, draw_button, adjust_difficulty
import sys

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

def show_instructions():
    instructions_running = True
    current_image_idx = 0  # Start with the first image

    while instructions_running:
        WIN.fill(INSTRUCTIONS_BACKGROUNDCOLOR)  # background color
        font = pygame.font.SysFont("Arial", 24)
        instructions_text = "Use the LEFT and RIGHT arrow keys to change images. Press any other key to return."

        # Render instruction text above the image
        text_surface = font.render(instructions_text, True, WHITE)
        WIN.blit(text_surface, (20, HEIGHT - 30))  # Adjust positioning as needed

        # Display the current instruction image
        WIN.blit(instruction_images[current_image_idx],
                 ((WIDTH - instruction_images[current_image_idx].get_width()) // 2, 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_image_idx = (current_image_idx - 1) % len(instruction_images)  # Go to the previous image
                elif event.key == pygame.K_RIGHT:
                    current_image_idx = (current_image_idx + 1) % len(instruction_images)  # Go to the next image
                else:
                    instructions_running = False  # Exit on any other key press

def show_difficulty_selection():
    global SELECTED_DIFFICULTY
    difficulties = ["Easy", "Medium", "Hard", "Extreme"]
    selected_difficulty_idx = 0
    selecting_difficulty = True

    while selecting_difficulty:
        WIN.fill(INSTRUCTIONS_BACKGROUNDCOLOR)  # background color
        WIN.blit(MAINMENU_BACKGROUND, (CENTER_X, CENTER_Y))
        font = pygame.font.SysFont("Arial", 50)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_difficulty_idx > 0:
                    selected_difficulty_idx -= 1
                elif event.key == pygame.K_DOWN and selected_difficulty_idx < len(difficulties) - 1:
                    selected_difficulty_idx += 1
                elif event.key == pygame.K_RETURN:
                    SELECTED_DIFFICULTY = difficulties[selected_difficulty_idx]
                    adjust_difficulty(SELECTED_DIFFICULTY)  # Adjust game settings based on selected difficulty
                    return  # Return to start the game

        # Render the difficulty options
        for idx, difficulty in enumerate(difficulties):
            color = WHITE if idx == selected_difficulty_idx else GRAY
            text = font.render(difficulty, True, color)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50 + idx * 60))

        pygame.display.update()


def main_menu():
    menu = True
    options = ["Start", "Instructions", "Sound options", "Quit"]
    selected_idx = 0
    sound_options = ["Sound ON", "Sound OFF"]
    selected_sound_idx = 0


    while menu:
        global SOUND_ON
        WIN.fill(INSTRUCTIONS_BACKGROUNDCOLOR)  # background color
        WIN.blit(MAINMENU_BACKGROUND, (CENTER_X, CENTER_Y))
        font = pygame.font.SysFont("Arial", 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_idx > 0:
                    selected_idx -= 1
                elif event.key == pygame.K_DOWN and selected_idx < len(options) - 1:
                    selected_idx += 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT and options[
                    selected_idx] == "Sound ON/OFF":
                    selected_sound_idx = (selected_sound_idx + 1) % 2  # Toggle sound option
                if event.key == pygame.K_RETURN:
                    if options[selected_idx] == "Start":
                        show_difficulty_selection()  # Show difficulty selection menu
                        menu = False  # Exit the main menu
                    elif options[selected_idx] == "Instructions":
                        show_instructions()  # Function to display instructions
                    elif options[selected_idx] == "Quit":
                        pygame.quit()
                        quit()

        # Render the main menu options
        for idx, option in enumerate(options):
            if option == "Sound options":
                display_text = f"{option}: {sound_options[selected_sound_idx]}"
                SOUND_ON = sound_options[selected_sound_idx] == "Sound ON"
            else:
                display_text = option
            color = WHITE if idx == selected_idx else GRAY
            text = font.render(display_text, True, color)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100 + idx * 60))

        pygame.display.update()

    # Modify the Shelf class to use the new width_range for generating shelf sizes
