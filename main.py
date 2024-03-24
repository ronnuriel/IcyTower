import sys
import pygame
import random

GAME_FPS = 150
WIDTH, HEIGHT = 1000, 700
JUMPING_HEIGHT = 20
MAX_ACCELERATION = 10
VEL_X = 3  # Setting the moving speed.
VEL_Y = JUMPING_HEIGHT  # Setting the jumping height.
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GAMEPLAY_SOUND_LENGTH = 31  # 31 seconds.
SHELVES_COUNT = 500  # Number of shelves in the game.
MAX_SHELF_NUMBER = 0

# Images:
BODY_IMAGE = pygame.image.load("Assets/body.png")
BACKGROUND = pygame.image.load("Assets/background.png")
BRICK_IMAGE = pygame.image.load("Assets/brick_block.png")
SHELF_BRICK_IMAGE = pygame.image.load("Assets/shelf_brick.png")

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

# Colors:
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def get_player_name():
    font = pygame.font.SysFont("Arial", 32)
    current_name = []
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)

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

        WIN.fill((0, 0, 0))  # Clear screen
        text_surf = font.render("Enter Name: " + ''.join(current_name), True, (255, 255, 255))
        WIN.blit(text_surf, (input_box.x - 20, input_box.y + 5))
        pygame.draw.rect(WIN, (255, 255, 255), input_box, 2)
        pygame.display.update()


def save_score(name, score):
    with open("leaderboard.txt", "a") as file:
        file.write(f"{name} {score}\n")


def show_leaderboard():
    try:
        with open("leaderboard.txt", "r") as file:
            scores = [line.strip().split(' ') for line in file]
            scores.sort(key=lambda x: int(x[1]), reverse=True)  # Sort scores in descending order
    except FileNotFoundError:
        scores = []

    running = True
    while running:
        WIN.fill((0, 0, 0))  # Clear screen
        font = pygame.font.SysFont("Arial", 24)
        title = font.render("Leaderboard", True, (255, 255, 255))
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

        for i, (name, score) in enumerate(scores[:10], start=1):  # Display top 10 scores
            text = font.render(f"{i}. {name} - {score}", True, (255, 255, 255))
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 30 + i * 30))

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


def main_menu():
    menu = True
    selected = "Easy"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "Easy"
                elif event.key == pygame.K_DOWN:
                    selected = "Medium"
                elif event.key == pygame.K_LEFT:
                    selected = "Hard"
                elif event.key == pygame.K_RIGHT:
                    selected = "Extreme"
                if event.key == pygame.K_RETURN:
                    return selected

        WIN.fill(BLACK)
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("Select Difficulty: " + selected, True, WHITE)
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()


def adjust_difficulty(difficulty):
    global BACKGROUND_ROLLING_SPEED, Shelf

    if difficulty == "Easy":
        BACKGROUND_ROLLING_SPEED = 1
        Shelf.width_range = (5, 8)  # Easier: Wider shelves
    elif difficulty == "Medium":
        BACKGROUND_ROLLING_SPEED = 2
        Shelf.width_range = (4, 7)
    elif difficulty == "Hard":
        BACKGROUND_ROLLING_SPEED = 3
        Shelf.width_range = (3, 6)  # Harder: Narrower shelves
    elif difficulty == "Extreme":
        BACKGROUND_ROLLING_SPEED = 4
        Shelf.width_range = (2, 5)  # Extreme: Very narrow shelves

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
    if num % 50 == 0:
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
    if direction == "Left":
        if body.x - body.acceleration >= LEFT_WALL_BOUND:  # If the body isn't about to pass the left wall on the next step.
            body.x -= body.acceleration  # Take the step.
        else:  # If the body is about to pass the left wall on the next step.
            body.x = LEFT_WALL_BOUND  # Force it to stay inside.
    else:  # If direction is right
        if body.x + body.acceleration <= RIGHT_WALL_BOUND - body.size:  # If the body isn't about to pass the right wall on the next step.
            body.x += body.acceleration  # Take the step.
        else:  # If the body is about to pass the right wall on the next step.
            body.x = RIGHT_WALL_BOUND - body.size  # Force the body to stay inside.
    body.acceleration -= 1  # Decreasing body's movement speed.


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
        for x in range(shelf.rect.x, shelf.rect.x + shelf.width, 32):
            WIN.blit(SHELF_BRICK_IMAGE, (x, shelf.rect.y))  # Drawing the shelf.
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
                    if current_standing_shelf != shelf.number and shelf.number % 50 == 0 and shelf.number != 0:
                        BACKGROUND_ROLLING_SPEED += 1  # Rolling speed increases every 50 shelves.
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


def GameOver():  # Quitting the game.
    print("Game Over")
    print("Your score is: ", MAX_SHELF_NUMBER)
    name = get_player_name()
    save_score(name, MAX_SHELF_NUMBER)
    show_leaderboard()
    pygame.quit()
    sys.exit(1)


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
    selected_difficulty = main_menu()
    adjust_difficulty(selected_difficulty)
    main()
