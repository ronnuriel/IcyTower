from Const import (WIDTH, HEIGHT, CENTER_X, CENTER_Y, INSTRUCTIONS_BACKGROUNDCOLOR, GAME_OVER_BACKGROUND
                   ,WIN,WHITE, instruction_images)
import pygame

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