from Const import (WIDTH, HEIGHT, BACKGROUND, SHELF_BRICK_IMAGE, SHELF_BRICK_IMAGE2, SHELF_BRICK_IMAGE3, BRICK_IMAGE,
                   WALL_WIDTH, WALLS_ROLLING_SPEED, WIN, BLACK, GRAY, BODY_IMAGE, body, total_shelves_list,
                   background_y, BACKGROUND_Y, WALLS_Y)
import pygame


def HandleBackground():  # Drawing the background.
    if body.y >= total_shelves_list[500].rect.y:
        WIN.blit(BACKGROUND, (32, background_y))


def DrawWindow():  # Basically, drawing the screen.
    global WALLS_Y
    font = pygame.font.SysFont("Arial", 26)
    HandleBackground()
    for shelf in total_shelves_list:
        if shelf.number < 20:
            shelf_image = SHELF_BRICK_IMAGE
        elif shelf.number < 40:
            shelf_image = SHELF_BRICK_IMAGE2
        else:
            shelf_image = SHELF_BRICK_IMAGE3

        for x in range(shelf.rect.x, shelf.rect.x + shelf.width, 32):
            WIN.blit(shelf_image, (x, shelf.rect.y))  # Drawing the shelf.
            if shelf.number % 10 == 0 and shelf.number != 0:
                shelf_number = pygame.Rect(shelf.rect.x + shelf.rect.width / 2 - 16, shelf.rect.y,
                                           16 * len(str(shelf.number)), 25)
                pygame.draw.rect(WIN, GRAY, shelf_number)
                txt = font.render(str(shelf.number), True, BLACK)
                WIN.blit(txt,
                         (shelf.rect.x + shelf.rect.width / 2 - 16, shelf.rect.y))  # Drawing the number of the shelf.
    for y in range(WALLS_Y, HEIGHT, 108):  # Drawing the walls.
        WIN.blit(BRICK_IMAGE, (0, y))
        WIN.blit(BRICK_IMAGE, (WIDTH - WALL_WIDTH, y))

    rotated_image = pygame.transform.rotate(BODY_IMAGE, body.angle)
    new_rect = rotated_image.get_rect(center=BODY_IMAGE.get_rect(topleft=(body.x, body.y)).center)

    WIN.blit(rotated_image, new_rect.topleft)  # Draw the rotated character
    pygame.display.update()


def ScreenRollDown():  # Increasing the y values of all elements.
    global background_y, WALLS_Y
    for shelf in total_shelves_list:
        shelf.rect.y += 1
    body.y += 1
    background_y += 0.5
    if background_y == BACKGROUND_Y + 164:
        background_y = BACKGROUND_Y
    WALLS_Y += WALLS_ROLLING_SPEED
    if WALLS_Y == 0:
        WALLS_Y = -108
