import pygame
import random
from typing import List

import Color


class Rectangle:
    window_width = 500
    window_heigth = 500

    def __init__(self, rectangle, color, background_color, win):
        self.rectangle = rectangle
        self.initial_pos = (rectangle.x, rectangle.y)
        self.color = color
        # TODO: Can be upgraded to multiple backgrounds
        self.background_color = background_color
        self.win = win
        self.draw()

    def __del__(self):
        self.draw_background()

    def get_rectangle_array(self):
        return (self.rectangle, self.color)

    def draw(self):
        pygame.draw.rect(self.win, self.color.get_color(), self.rectangle)

    def draw_background(self):
        pygame.draw.rect(
            self.win, self.background_color.get_color(), self.rectangle)

    def is_collision(self, character_b):
        return self.rectangle.colliderect(character_b.rectangle)

    def move(self, dx, dy, blockings):
        # Move each axis separately.
        # Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0, blockings)
        if dy != 0:
            self.move_single_axis(0, dy, blockings)

    def move_single_axis(self, dx, dy, blockings):
        self.draw_background()

        self.rectangle.x += dx
        self.rectangle.y += dy

        for block in blockings:
            if self.is_collision(block):
                if dx > 0:  # Moving right; Hit the left side of the block
                    self.rectangle.right = block.rectangle.left
                if dx < 0:  # Moving left; Hit the right side of the block
                    self.rectangle.left = block.rectangle.right
                if dy > 0:  # Moving down; Hit the top side of the block
                    self.rectangle.bottom = block.rectangle.top
                if dy < 0:  # Moving up; Hit the bottom side of the block
                    self.rectangle.top = block.rectangle.bottom
        self.draw()

    def reset_position(self, x, y):
        self.draw_background()
        self.rectangle.x = self.initial_pos[0]
        self.rectangle.y = self.initial_pos[1]
        self.draw()


def random_spanner(amount: int, delimiter_rect: pygame.Rect,
                   span_rect: pygame.Rect, color: Color.RBGColor,
                   background_color: Color.RBGColor,
                   win: pygame.Surface, is_blocking: bool,
                   blockings: List[Rectangle]) -> List[Rectangle]:
    final_list = list()
    min_x = delimiter_rect.x
    min_y = delimiter_rect.y
    max_x = delimiter_rect.x + delimiter_rect.width - span_rect.width
    max_y = delimiter_rect.y + delimiter_rect.height - span_rect.height

    while len(final_list) < amount:
        current_x = random.randint(min_x, max_x)
        current_y = random.randint(min_y, max_y)

        current_rectangle = pygame.Rect(current_x, current_y,
                                        span_rect.width, span_rect.height)
        blocks = False
        for blocking in blockings:
            if current_rectangle.colliderect(blocking.rectangle) is True:
                blocks = True
                break

        if blocks is False:
            final_list.append(Rectangle(current_rectangle,
                                        color,
                                        background_color,
                                        win))
            if is_blocking:
                blockings.append(final_list[-1])

    return final_list
