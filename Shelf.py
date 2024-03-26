from Const import *
import random
from main import total_shelves_list, body, GameOver
class Shelf:
    width_range = (4, 7)  # This will get overwritten based on difficulty

    def __init__(self, number):
        self.number = number
        self.width = random.randint(*self.width_range) * 32
        self.x = random.randint(LEFT_WALL_BOUND, RIGHT_WALL_BOUND - self.width)
        self.y = -number * 130 + HEIGHT - 25
        self.rect = pygame.Rect(self.x, self.y, self.width, 32)

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