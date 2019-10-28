import pygame
import random
from typing import List

import Color
import Rectangle

pygame.init()

delay_ms = 100
win_heigth = 700
win_width = 1200
win_title = "First game"
win_life = True

vel = 5
possible_movements = ["UP", "RIGHT", "DOWN", "LEFT"]
number_of_characters = 20
number_of_foods = 20
characters = list()
mov = list()

win = pygame.display.set_mode((win_width, win_heigth))
pygame.display.set_caption(win_title)

blocking_rects = list()
stage = list()
foods = list()
window_rect = pygame.Rect(0, 0, win_width, win_heigth)
stage_rects = (pygame.Rect(0, 0, 100, win_heigth),
               pygame.Rect(0, 0, win_width, 100),
               pygame.Rect(1100, 0, 100, win_heigth),
               pygame.Rect(0, 600, win_width, 100))
actual_stage_rect = (pygame.Rect(100, 100, 1000, 500))
rect_1 = pygame.Rect(0, 0, 10, 15)
rect_2 = pygame.Rect(0, 0, 5, 5)

color_1 = Color.RBGColor(255, 0, 0)
color_2 = Color.RBGColor(0, 0, 255)
food_color = Color.RBGColor(255, 255, 255)
stage_color = Color.RBGColor(211, 211, 211)
stage_walls_color = Color.RBGColor(0, 0, 0)

stage.append(Rectangle.Rectangle(actual_stage_rect,
                                 stage_color, stage_walls_color, win))

characters = Rectangle.random_spanner(number_of_characters, actual_stage_rect,
                                      rect_1, color_1, stage_color, win, True,
                                      blocking_rects)

foods = Rectangle.random_spanner(number_of_foods, actual_stage_rect, rect_2,
                                 food_color, stage_color, win, False,
                                 blocking_rects)

for stage_rect in stage_rects:
    stage.append(Rectangle.Rectangle(
        stage_rect, stage_walls_color, stage_walls_color, win))
    blocking_rects.append(stage[-1])

for i in range(number_of_characters):
    mov.append(random.choice(possible_movements))

while win_life:
    # Use actual timer later on
    pygame.time.delay(delay_ms)
    pygame.display.update()

    if characters[0].is_collision(characters[1]):
        pygame.time.delay(delay_ms+1000)
        characters[0].reset_position(50, 50)
        characters[1].reset_position(120, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_life = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        characters[0].move(0, -vel, blocking_rects[1:])
    elif keys[pygame.K_RIGHT]:
        characters[0].move(vel, 0, blocking_rects[1:])
    elif keys[pygame.K_DOWN]:
        characters[0].move(0, vel, blocking_rects[1:])
    elif keys[pygame.K_LEFT]:
        characters[0].move(-vel, 0, blocking_rects[1:])
'''
    for i in range(number_of_characters):
        mov[i] = random.choice(possible_movements)
        while characters[i].is_within_limits(mov[i], stage_rect) is False:
            mov[i] = random.choice(possible_movements)
        characters[i].move(mov[i])
'''

pygame.display.update()
pygame.time.delay(delay_ms)
pygame.quit()
