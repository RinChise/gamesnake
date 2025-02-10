import sys
from typing import Optional, Tuple
import pygame
from src.logic import BaseLogic, COLORS


class SingleplayerLogic(BaseLogic):
    def __init__(self, game_window: pygame.Surface, fps_controller: pygame.time.Clock, window_width: int, window_height: int):
        """
        Initializes single-player game logic.
        """
        super().__init__(game_window, fps_controller, window_width, window_height)
        self.game_over_flag = False
        center_x = (window_width // 2 // self.block_size) * self.block_size
        center_y = ((self.playable_height // 2) // self.block_size) * self.block_size + self.border_height
        self.snake_pos = [center_x, center_y]
        self.snake_body = [
            self.snake_pos[:],
            [center_x - self.block_size, center_y],
            [center_x - 2 * self.block_size, center_y]
        ]
        self.food_pos = self.spawn_food(self.snake_body)
        self.food_spawn = True
        self.direction = "RIGHT"
        self.change_to = self.direction

    def process_events(self) -> None:
        """
        Handles keyboard events for single-player.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """
        Updates the snake's direction based on key presses.
        """
        if event.key in (pygame.K_UP, pygame.K_w):
            self.change_to = "UP"
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.change_to = "DOWN"
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.change_to = "LEFT"
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.change_to = "RIGHT"

    def update_direction(self) -> None:
        """
        Updates the snake's direction while preventing 180° turns.
        """
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def update_snake_position(self) -> None:
        """
        Moves the snake based on the current direction.
        """
        if self.direction == "UP":
            self.snake_pos[1] -= self.block_size
        elif self.direction == "DOWN":
            self.snake_pos[1] += self.block_size
        elif self.direction == "LEFT":
            self.snake_pos[0] -= self.block_size
        elif self.direction == "RIGHT":
            self.snake_pos[0] += self.block_size

    def update_snake_body(self) -> None:
        """
        Updates the snake's body and checks if food is eaten.
        """
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos == self.food_pos:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        if not self.food_spawn:
            self.food_pos = self.spawn_food(self.snake_body)
            self.food_spawn = True

    def check_collisions(self) -> bool:
        """
        Checks for collisions with walls or the snake's body.
        """
        if (self.snake_pos[0] < 0 or
                self.snake_pos[0] >= self.window_width or
                self.snake_pos[1] < self.border_height or
                self.snake_pos[1] >= self.window_height):
            return True

        if self.snake_pos in self.snake_body[1:]:
            return True

        return False

    def draw_elements(self, colors: Optional[Tuple[Tuple[int, int, int], ...]] = None) -> None:
        """
        Draws the game elements: snake and food.
        """
        if colors is None or len(colors) < 5:
            colors = (COLORS["BLACK"], COLORS["RED"], COLORS["MAGENTA"], COLORS["BLUE"], COLORS["WHITE"])
        black, red, magenta, blue, white = colors

        self.game_window.fill(black, (0, self.border_height, self.window_width, self.playable_height))

        # Draw the snake
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, blue, pygame.Rect(pos[0], pos[1], self.block_size, self.block_size))

        # Draw the food
        pygame.draw.rect(self.game_window, magenta, pygame.Rect(self.food_pos[0], self.food_pos[1], self.block_size, self.block_size))

        # Draw the border and score
        self.draw_border_and_score()

        pygame.display.update()
