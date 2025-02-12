import pygame
import sys
import time
import random
from typing import List, Tuple, Optional

# Konstanten für Farben und Schriftarten
COLORS = {
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "MAGENTA": (255, 6, 254),
    "BLUE": (0, 255, 255),
    "WHITE": (255, 255, 255),
    "GRAY": (50, 50, 50),
    "LIGHT_SKY_BLUE": (135, 206, 250),
    "DODGER_BLUE": (30, 144, 255),
}

FONT_NAME = "arial"
FONT_SIZE_SCORE = 30
FONT_SIZE_GAME_OVER = 50

class BaseLogic:
    DEFAULT_COLORS = (COLORS["BLACK"], COLORS["RED"], COLORS["MAGENTA"], COLORS["BLUE"], COLORS["WHITE"])

    def __init__(self, game_window: pygame.Surface, fps_controller: pygame.time.Clock, window_width: int, window_height: int):
        """
        Shared initialization for all game logic classes.
        """
        self.game_window = game_window
        self.fps_controller = fps_controller
        self.window_width = window_width
        self.window_height = window_height
        self.border_height = 50
        self.block_size = 10
        self.playable_height = self.window_height - self.border_height
        self.score = 0

    def spawn_food(self, snake_bodies: List[List[List[int]]]) -> List[int]:
        """
        Generates a new food position that is not in any of the snakes' bodies.
        """
        if self.food_pos is None:  # Only spawn if no food exists
            while True:
                new_food_pos = [
                    random.randrange(0, self.window_width // self.block_size) * self.block_size,
                    random.randrange(self.border_height // self.block_size,
                                     self.window_height // self.block_size) * self.block_size
                ]
                if all(new_food_pos not in body for body in snake_bodies):
                    self.food_pos = new_food_pos  # Store food position in BaseLogic
                    break  # Exit the loop once a valid position is found

    def draw_border_and_score(self) -> None:
        """
        Draws the score border and displays the current score.
        """
        pygame.draw.rect(self.game_window, COLORS["GRAY"], (0, 0, self.window_width, self.border_height))
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SCORE)
        score_surface = font.render(f"P: {self.score}", True, COLORS["WHITE"])
        self.game_window.blit(score_surface, (10, 10))

    def draw_elements(self, colors: Optional[Tuple[Tuple[int, int, int], ...]] = None) -> None:
        """
        Draws the game elements: background, border, and score.
        """
        if colors is None or len(colors) < 5:
            colors = (COLORS["BLACK"], COLORS["RED"], COLORS["MAGENTA"], COLORS["BLUE"], COLORS["WHITE"])
        black, red, magenta, blue, white = colors

        # Clear the playable area
        self.game_window.fill(black, (0, self.border_height, self.window_width, self.playable_height))

        # Draw the border and score
        self.draw_border_and_score()

        pygame.display.update()

    def game_over(self, colors: Optional[Tuple[Tuple[int, int, int], ...]] = None) -> int:
        """
        Displays the game over screen and returns the final score.
        """
        if colors is None or len(colors) < 5:
            colors = (COLORS["BLACK"], COLORS["RED"], COLORS["MAGENTA"], COLORS["BLUE"], COLORS["WHITE"])
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

