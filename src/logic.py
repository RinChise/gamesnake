import pygame
import sys
import time
import random
from typing import List, Tuple, Optional

# Constants (Consider moving these to a separate constants.py file)
COLORS = { "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "MAGENTA": (255, 6, 254),
    "BLUE": (0, 255, 255),
    "WHITE": (255, 255, 255),
    "GRAY": (50, 50, 50),
    "LIGHT_SKY_BLUE": (135, 206, 250),
    "DODGER_BLUE": (30, 144, 255)
}

FONT_NAME = "arial"
FONT_SIZE_SCORE = 30
FONT_SIZE_GAME_OVER = 50

class BaseLogic:
    DEFAULT_COLORS = (COLORS["BLACK"], COLORS["RED"], COLORS["MAGENTA"], COLORS["BLUE"], COLORS["WHITE"])

    def __init__(self, game_window: pygame.Surface, fps_controller: pygame.time.Clock, window_width: int, window_height: int):
        self.game_window = game_window
        self.fps_controller = fps_controller
        self.window_width = window_width
        self.window_height = window_height
        self.border_height = 50
        self.block_size = 10
        self.playable_height = self.window_height - self.border_height
        self.score = 0
        self.food_pos = [] # initialize as list to handle multiple food items

    def spawn_food(self, snake_bodies: List[List[List[int]]], num_food_items: int = 2) -> None:
        """Generates new food positions that are not in any of the snakes' bodies."""

        self.food_pos = [] # clear food positions
        while len(self.food_pos) < num_food_items:  # Use num_food_items
            new_food_pos = [
                random.randrange(0, self.window_width // self.block_size) * self.block_size,
                random.randrange(self.border_height // self.block_size,
                                 self.window_height // self.block_size) * self.block_size
            ]
            if all(new_food_pos not in body for body in snake_bodies) and new_food_pos not in self.food_pos:
                self.food_pos.append(new_food_pos)

    def draw_border_and_score(self) -> None:
        pygame.draw.rect(self.game_window, COLORS["GRAY"], (0, 0, self.window_width, self.border_height))
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SCORE)
        score_surface = font.render(f"Score: {self.score}", True, COLORS["WHITE"]) # placeholder, will be overwritten
        self.game_window.blit(score_surface, (10, 10))

    def draw_elements(self, colors: Optional[Tuple[Tuple[int, int, int], ...]] = None) -> None:
        if colors is None:
            colors = self.DEFAULT_COLORS
        black, red, magenta, blue, white = colors

        self.game_window.fill(black, (0, self.border_height, self.window_width, self.playable_height)) # fill the playable area
        self.draw_border_and_score() # draw border and score

    def game_over(self, colors: Optional[Tuple[Tuple[int, int, int], ...]] = None) -> int:
        if colors is None:
            colors = self.DEFAULT_COLORS
        black, red, magenta, blue, white = colors

        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_GAME_OVER)
        game_over_surface = font.render('Game Over', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_width // 2, self.window_height // 4)
        self.game_window.fill(black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.draw_border_and_score()
        pygame.display.flip()
        time.sleep(1)
        return self.score