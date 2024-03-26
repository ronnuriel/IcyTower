import sys
import pygame
import random
from Const import *
from Body import Body
from Shelf import OnShelf, Shelf
from Menu import main_menu, get_player_name
from Scores import save_score, show_leaderboard


pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


body = Body()

total_shelves_list = []
for num in range(0, SHELVES_COUNT + 1):  # Creating all the game shelves.
    new_shelf = Shelf(num)
    if num % LEVEL_UP == 0:
        new_shelf.width = BACKGROUND_WIDTH
        new_shelf.rect.width = BACKGROUND_WIDTH
        new_shelf.x = WALL_WIDTH
        new_shelf.rect.x = WALL_WIDTH
    total_shelves_list.append(new_shelf)


def Move(direction):  # Moving the body according to the wanted direction.
    global body

    bounce_back_distance = 20  # Increased bounce back distance for a stronger bounce effect
    bounce_reduction_factor = 3  # How much to reduce acceleration by (smaller values = stronger bounce)

    if direction == "Left":
        # Check if the body is about to pass the left wall on the next step
        if body.x - body.acceleration < LEFT_WALL_BOUND:
            body.x = LEFT_WALL_BOUND + bounce_back_distance  # Bounce back from the wall
            body.acceleration = -(body.acceleration // bounce_reduction_factor)  # Stronger bounce effect
        else:
            body.x -= body.acceleration  # Normal movement
    else:  # If direction is "Right"
        # Check if the body is about to pass the right wall on the next step
        if body.x + body.acceleration + body.size > RIGHT_WALL_BOUND:
            body.x = RIGHT_WALL_BOUND - body.size - bounce_back_distance  # Bounce back from the wall
            body.acceleration = -(body.acceleration // bounce_reduction_factor)  # Stronger bounce effect
        else:
            body.x += body.acceleration  # Normal movement

    # Always decrease the body's acceleration each frame to simulate friction
    body.acceleration = max(0, abs(body.acceleration) - 1) * (1 if body.acceleration > 0 else -1)


def HandleMovement(keys_pressed):  # Handling the Left/Right buttons pressing.
    global body, new_movement, current_direction
    if keys_pressed[pygame.K_LEFT] and body.x > LEFT_WALL_BOUND:  # If pressed "Left", and body is inside the bounding.
        current_direction = "Left"
        if body.acceleration + 3 <= MAX_ACCELERATION:  # If body's movement speed isn't maxed.
            body.acceleration += 3  # Accelerating the body's movement speed.
        else:
            body.acceleration = MAX_ACCELERATION
    if keys_pressed[
        pygame.K_RIGHT] and body.x < RIGHT_WALL_BOUND:  # If pressed "Right", and body is inside the bounding.
        current_direction = "Right"
        if body.acceleration + 3 <= MAX_ACCELERATION:  # If body's movement speed isn't maxed.
            body.acceleration += 3  # Accelerating the body's movement speed.
        else:
            body.acceleration = MAX_ACCELERATION


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


def draw_button(text, position, size, is_hovered):
    font = pygame.font.SysFont("Arial", 32)
    text_surf = font.render(text, True, BLACK if is_hovered else WHITE)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(WIN, YELLOW if is_hovered else GRAY, button_rect)
    text_rect = text_surf.get_rect(center=button_rect.center)
    WIN.blit(text_surf, text_rect)
    return button_rect


def GameOver():
    print("Game Over")
    print("Your score is: ", MAX_SHELF_NUMBER)
    name = get_player_name()

    if name == "":
        name = "Anonymous"

    save_score(name, MAX_SHELF_NUMBER, SELECTED_DIFFICULTY)
    show_leaderboard()

    pygame.display.update()


def CheckIfTouchingFloor():  # Checking if the body is still on the main ground.
    global standing, falling
    if body.y > HEIGHT - body.size:
        if not rolling_down:  # Still on the starting point of the game, can't lose yet.
            body.y = HEIGHT - body.size
            standing, falling = True, False
        else:  # In a more advanced part of the game, when can already lose.
            GameOver()


def HandleBackground():  # Drawing the background.
    if body.y >= total_shelves_list[500].rect.y:
        WIN.blit(BACKGROUND, (32, background_y))

def adjust_difficulty(difficulty):
    global SELECTED_DIFFICULTY
    SELECTED_DIFFICULTY = None
    global BACKGROUND_ROLLING_SPEED, Shelf

    if difficulty == "Easy":
        SELECTED_DIFFICULTY = "Easy"
        BACKGROUND_ROLLING_SPEED = 1
        Shelf.width_range = (7, 9)  # Easier: Wider shelves
    elif difficulty == "Medium":
        SELECTED_DIFFICULTY = "Medium"
        BACKGROUND_ROLLING_SPEED = 2
        Shelf.width_range = (5, 8)
    elif difficulty == "Hard":
        SELECTED_DIFFICULTY = "Hard"
        BACKGROUND_ROLLING_SPEED = 3
        Shelf.width_range = (3, 6)  # Harder: Narrower shelves
    elif difficulty == "Extreme":
        SELECTED_DIFFICULTY = "Extreme"
        BACKGROUND_ROLLING_SPEED = 4
        Shelf.width_range = (1, 2)  # Extreme: Very narrow shelves

def main():  # Main function.
    global body, keys_pressed, total_shelves_list, jumping, standing, falling, rolling_down, new_movement
    game_running = True
    rolling_down = False
    paused = False
    sound_timer = 0
    while game_running:
        while game_running and not paused:
            on_ground = not rolling_down and body.y == HEIGHT - 25 - body.size
            if sound_timer % (56 * GAMEPLAY_SOUND_LENGTH) == 0:  # 56 = Program loops count per second.
                if SOUND_ON:
                    GAMEPLAY_SOUND.play()
            sound_timer += 1
            if rolling_down:  # If screen should roll down.
                for _ in range(BACKGROUND_ROLLING_SPEED):
                    ScreenRollDown()
            DrawWindow()  # Draw shelves, body and background.
            keys_pressed = pygame.key.get_pressed()
            HandleMovement(keys_pressed)  # Moving according to the pressed buttons.
            if body.acceleration != 0:  # If there's any movement.
                Move(current_direction)

            if keys_pressed[pygame.K_SPACE] and (
                    standing or on_ground):  # If enter "Space" and currently not in mid-jump.
                body.vel_y = VEL_Y  # Resets the body's jumping velocity.
                jumping, standing, falling = True, False, False

                jumping, standing, falling = True, False, False

            if jumping and body.vel_y >= 0:  # Jumping up.
                if body.vel_y == VEL_Y:  # First moment of the jump.
                    if SOUND_ON:
                        JUMPING_SOUND.play()
                print("Jumping...")
                body.y -= body.vel_y
                body.vel_y -= 1
                if body.y <= HEIGHT / 5:  # If the body get to the top quarter of the screen.
                    rolling_down = True  # Starts rolling down the screen.
                    for _ in range(10):  # Rolling 10 times -> Rolling faster, so he can't pass the top of the screen.
                        ScreenRollDown()
                if not body.vel_y:  # Standing in the air.
                    jumping, standing, falling = False, False, True
            if falling:  # Falling down.
                if OnShelf():  # Standing on a shelf.
                    print("Standing...")
                    jumping, standing, falling = False, True, False
                else:  # Not standing - keep falling down.
                    print("Falling...")
                    body.y -= body.vel_y
                    body.vel_y -= 1
            CheckIfTouchingFloor()

            if standing and not OnShelf() and not on_ground:  # If falling from a shelf.
                print("Falling from shelf...")
                body.vel_y = 0  # Falls slowly from the shelf and not as it falls at the end of a jumping.
                body.angle = 0
                standing, falling = False, True

            if jumping and body.acceleration != 0:
                body.angle += 20  # Adjust this value to control the speed of the spin
            else:
                body.angle = 0  # Reset the angle when not jumping

            if body.acceleration == MAX_ACCELERATION - 1:  # While on max acceleration, getting a jumping height boost.
                VEL_Y = JUMPING_HEIGHT + 5
            else:  # If not on max acceleration.
                VEL_Y = JUMPING_HEIGHT  # Back to normal jumping height.

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
            pygame.time.Clock().tick(GAME_FPS)


if __name__ == "__main__":
    main_menu()
    adjust_difficulty(SELECTED_DIFFICULTY)
    main()
