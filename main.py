import sys
import pygame
import random

GAME_FPS = 150
WIDTH, HEIGHT = 800, 600
JUMPING_HEIGHT = 20
MAX_ACCELERATION = 10
VEL_X = 3  # Setting the moving speed.
VEL_Y = JUMPING_HEIGHT  # Setting the jumping height.
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GAMEPLAY_SOUND_LENGTH = 31  # 31 seconds.
SHELVES_COUNT = 500  # Number of shelves in the game.
MAX_SHELF_NUMBER = 0

# Constants:
LEVEL_UP = 30
# Colors:
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
INSTRUCTIONS_BACKGROUNDCOLOR = (150, 195, 213, 255)

# Images:
BODY_IMAGE = pygame.image.load("Assets/icyMan.png")
BACKGROUND = pygame.image.load("Assets/background2.jpg")
BRICK_IMAGE = pygame.image.load("Assets/brick_block.png")
SHELF_BRICK_IMAGE = pygame.image.load("Assets/shelf_brick.png")
SHELF_BRICK_IMAGE2 = pygame.image.load("Assets/ice.png")
SHELF_BRICK_IMAGE3 = pygame.image.load("Assets/fire.png.webp")
MAINMENU_BACKGROUND = pygame.transform.scale(pygame.image.load("Assets/IcyTowerBackground.gif"), (WIDTH, HEIGHT))
CENTER_X = (WIDTH - MAINMENU_BACKGROUND.get_width()) // 2
CENTER_Y = (HEIGHT - MAINMENU_BACKGROUND.get_height()) // 2
GAME_OVER_BACKGROUND = pygame.transform.scale(pygame.image.load("Assets/game_over.png"), (WIDTH, HEIGHT))
GAME_OVER_BACKGROUND.set_colorkey(BLACK)
instruction_images = [
    pygame.transform.scale(pygame.image.load(r"Assets\game_instructions_goal.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(r"Assets\game_instructions_howTo.png"), (WIDTH, HEIGHT))

]

new_width = 800
new_height = 600

for i in range(len(instruction_images)):
    instruction_images[i] = pygame.transform.scale(instruction_images[i], (new_width, new_height))

new_width = 64
new_height = 64
# Resize the sprite
BODY_IMAGE = pygame.transform.scale(BODY_IMAGE, (new_width, new_height))

new_height = 32
new_width = 32
SHELF_BRICK_IMAGE2 = pygame.transform.scale(SHELF_BRICK_IMAGE2, (new_width, new_height))
SHELF_BRICK_IMAGE3 = pygame.transform.scale(SHELF_BRICK_IMAGE3, (new_width, new_height))

# Walls settings:
WALLS_Y = -128
WALL_WIDTH = 128
WALLS_ROLLING_SPEED = 2
RIGHT_WALL_BOUND = WIDTH - WALL_WIDTH
LEFT_WALL_BOUND = WALL_WIDTH

# Background settings:
BACKGROUND_WIDTH = WIDTH - 2 * WALL_WIDTH  # 2*64 is for two walls on the sides.
BACKGROUND_ROLLING_SPEED = 1
BACKGROUND_Y = HEIGHT - BACKGROUND.get_height()
background_y = BACKGROUND_Y

# Booleans:
jumping = False
falling = False
standing = False
rolling_down = False
new_movement = False
current_direction = None
current_standing_shelf = 0



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

    # Modify the Shelf class to use the new width_range for generating shelf sizes


class Shelf:
    width_range = (4, 7)  # This will get overwritten based on difficulty

    def __init__(self, number):
        self.number = number
        self.width = random.randint(*self.width_range) * 32
        self.x = random.randint(LEFT_WALL_BOUND, RIGHT_WALL_BOUND - self.width)
        self.y = -number * 130 + HEIGHT - 25
        self.rect = pygame.Rect(self.x, self.y, self.width, 32)


class Body:
    def __init__(self):
        self.size = 64
        self.x = WIDTH / 2 - self.size / 2
        self.y = HEIGHT - 25 - self.size
        self.vel_y = 0
        self.acceleration = 0
        self.angle = 0
        self.jumpable = self.vel_y <= 0  # If body is hitting a level, then it can jump only if the body is going down.


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

# Sounds:
SOUND_ON = False
JUMPING_SOUND = pygame.mixer.Sound("Assets/jumping_sound.wav")
GAMEPLAY_SOUND = pygame.mixer.Sound("Assets/gameplay_sound.wav")
HOORAY_SOUND = pygame.mixer.Sound("Assets/hooray_sound.wav")


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


def OnShelf():  # Checking whether the body is on a shelf, returning True/False.
    global jumping, standing, falling, BACKGROUND_ROLLING_SPEED, current_standing_shelf, MAX_SHELF_NUMBER

    if body.vel_y <= 0:  # Means the body isn't moving upwards, so now it's landing.
        for shelf in total_shelves_list:
            if body.y <= shelf.rect.y - body.size <= body.y - body.vel_y:  # If y values collide.shelf.rect.y - body.size >= body.y and shelf.rect.y - body.size <= body.y - body.vel_y
                if body.x + body.size * 2 / 3 >= shelf.rect.x and body.x + body.size * 1 / 3 <= shelf.rect.x + shelf.width:  # if x values collide.
                    body.y = shelf.rect.y - body.size
                    if current_standing_shelf != shelf.number and shelf.number % LEVEL_UP == 0 and shelf.number != 0:
                        BACKGROUND_ROLLING_SPEED += 1  # Rolling speed increases every 30 shelves.
                        current_standing_shelf = shelf.number
                    if shelf.number % 100 == 0 and shelf.number != 0:
                        if SOUND_ON:
                            HOORAY_SOUND.play()
                    if shelf.number == SHELVES_COUNT:
                        GameOver()
                    MAX_SHELF_NUMBER = shelf.number
                    return True
    else:  # Means body in not on a shelf.
        jumping, standing, falling = False, False, True


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
