import random
import pygame
import sys
from typing import Optional, Tuple, List
from src.logic import BaseLogic, COLORS, FONT_NAME, FONT_SIZE_SCORE


class MultiplayerLogic(BaseLogic):
    def __init__(self, game_window: pygame.Surface, fps_controller: pygame.time.Clock, window_width: int, window_height: int, player1_name: str, player2_name: str):
        super().__init__(game_window, fps_controller, window_width, window_height)
        self.game_over_flag = False
        self.player1_name = player1_name
        self.player2_name = player2_name

        center_x = (window_width // 2 // self.block_size) * self.block_size
        center_y = ((self.playable_height // 2) // self.block_size) * self.block_size + self.border_height
        offset = 5 * self.block_size

        # Initialize player 1
        self.snake1_pos = [center_x, center_y]
        self.snake1_body = [self.snake1_pos[:], [center_x - self.block_size, center_y], [center_x - 2 * self.block_size, center_y]]
        self.direction1 = "RIGHT"
        self.change_to1 = self.direction1
        self.score1 = 0

        # Initialize player 2
        self.snake2_pos = [center_x + offset, center_y]
        self.snake2_body = [self.snake2_pos[:], [center_x + offset - self.block_size, center_y], [center_x + offset - 2 * self.block_size, center_y]]
        self.direction2 = "RIGHT"
        self.change_to2 = self.direction2
        self.score2 = 0

        self.spawn_food([self.snake1_body, self.snake2_body])

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        # Player 1
        if event.key == pygame.K_UP:
            self.change_to1 = "UP"
        elif event.key == pygame.K_DOWN:
            self.change_to1 = "DOWN"
        elif event.key == pygame.K_LEFT:
            self.change_to1 = "LEFT"
        elif event.key == pygame.K_RIGHT:
            self.change_to1 = "RIGHT"

        # Player 2
        if event.key == pygame.K_w:
            self.change_to2 = "UP"
        elif event.key == pygame.K_s:
            self.change_to2 = "DOWN"
        elif event.key == pygame.K_a:
            self.change_to2 = "LEFT"
        elif event.key == pygame.K_d:
            self.change_to2 = "RIGHT"

    def update_direction(self) -> None:
        # Player 1
        if self.change_to1 == "UP" and self.direction1 != "DOWN":
            self.direction1 = "UP"
        elif self.change_to1 == "DOWN" and self.direction1 != "UP":
            self.direction1 = "DOWN"
        elif self.change_to1 == "LEFT" and self.direction1 != "RIGHT":
            self.direction1 = "LEFT"
        elif self.change_to1 == "RIGHT" and self.direction1 != "LEFT":
            self.direction1 = "RIGHT"

        # Player 2
        if self.change_to2 == "UP" and self.direction2 != "DOWN":
            self.direction2 = "UP"
        elif self.change_to2 == "DOWN" and self.direction2 != "UP":
            self.direction2 = "DOWN"
        elif self.change_to2 == "LEFT" and self.direction2 != "RIGHT":
            self.direction2 = "LEFT"
        elif self.change_to2 == "RIGHT" and self.direction2 != "LEFT":
            self.direction2 = "RIGHT"

    def update_snake_position(self) -> None:
        # Player 1
        if self.direction1 == "UP":
            self.snake1_pos[1] -= self.block_size
        elif self.direction1 == "DOWN":
            self.snake1_pos[1] += self.block_size
        elif self.direction1 == "LEFT":
            self.snake1_pos[0] -= self.block_size
        elif self.direction1 == "RIGHT":
            self.snake1_pos[0] += self.block_size

        # Player 2
        if self.direction2 == "UP":
            self.snake2_pos[1] -= self.block_size
        elif self.direction2 == "DOWN":
            self.snake2_pos[1] += self.block_size
        elif self.direction2 == "LEFT":
            self.snake2_pos[0] -= self.block_size
        elif self.direction2 == "RIGHT":
            self.snake2_pos[0] += self.block_size

    def update_snake_body(self) -> None:
        # Player 1
        if self.snake1_body:
            self.snake1_body.insert(0, list(self.snake1_pos))
            for i in range(len(self.food_pos)):
                if self.snake1_pos == self.food_pos[i] and self.food_pos[i] is not None:
                    self.score1 += 1
                    self.food_pos[i] = None  # Remove the eaten food
                    self.spawn_food([self.snake1_body, self.snake2_body], 1)  # Respawn only 1 food
                    break  # Important: Exit the loop after eating a food
            else:
                self.snake1_body.pop()

        # Player 2
        if self.snake2_body:
            self.snake2_body.insert(0, list(self.snake2_pos))
            for i in range(len(self.food_pos)):
                if self.snake2_pos == self.food_pos[i] and self.food_pos[i] is not None:
                    self.score2 += 1
                    self.food_pos[i] = None  # Remove the eaten food
                    self.spawn_food([self.snake1_body, self.snake2_body], 1)  # Respawn only 1 food
                    break  # Important: Exit the loop after eating a food
            else:
                self.snake2_body.pop()

    def spawn_food(self, snake_bodies: List[List[List[int]]], num_food_items: int = 1) -> None: # changed default to 1
        """Generates new food positions for only the missing food items."""
        while len(list(filter(None, self.food_pos))) < 2:  # Ensure there are always 2 food items (filter None values)
            new_food_pos = [
                random.randrange(0, self.window_width // self.block_size) * self.block_size,
                random.randrange(self.border_height // self.block_size,
                                 self.window_height // self.block_size) * self.block_size
            ]
            if all(new_food_pos not in body for body in snake_bodies) and new_food_pos not in self.food_pos:
                self.food_pos.append(new_food_pos)

    def check_collisions(self) -> None:
        """Checks for collisions, handles wrapping, and snake removal."""
        # Player 1 collisions and wrapping
        if self.snake1_body:  # Only check if snake exists
            if self.snake1_pos[0] < 0:
                self.snake1_pos[0] = self.window_width - self.block_size
            elif self.snake1_pos[0] >= self.window_width:
                self.snake1_pos[0] = 0
            elif self.snake1_pos[1] < self.border_height:
                self.snake1_pos[1] = self.window_height - self.block_size
            elif self.snake1_pos[1] >= self.window_height:
                self.snake1_pos[1] = self.border_height

            if self.snake1_pos in self.snake1_body[1:]:  # Self-collision (after wrapping)
                self.snake1_body = []  # Remove snake 1

        # Player 2 collisions and wrapping
        if self.snake2_body:  # Only check if snake exists
            if self.snake2_pos[0] < 0:
                self.snake2_pos[0] = self.window_width - self.block_size
            elif self.snake2_pos[0] >= self.window_width:
                self.snake2_pos[0] = 0
            elif self.snake2_pos[1] < self.border_height:
                self.snake2_pos[1] = self.window_height - self.block_size
            elif self.snake2_pos[1] >= self.window_height:
                self.snake2_pos[1] = self.border_height

            if self.snake2_pos in self.snake2_body[1:]:  # Self-collision (after wrapping)
                self.snake2_body = []  # Remove snake 2

        # Snake vs. Snake collisions (only if both snakes exist and AFTER wrapping)
        if self.snake1_body and self.snake2_body:
            snake1_body_copy = self.snake1_body[:]  # Create copies to avoid modifying while iterating
            snake2_body_copy = self.snake2_body[:]

            for i in range(len(snake1_body_copy)):
                for j in range(len(snake2_body_copy)):
                    if snake1_body_copy[i] == snake2_body_copy[j]:
                        if len(self.snake1_body) > len(self.snake2_body):  # Remove the bigger snake
                            self.snake2_body = []
                            self.winner = 1  # player 1 wins
                            self.game_over_flag = True
                        elif len(self.snake2_body) > len(self.snake1_body):
                            self.snake1_body = []
                            self.winner = 2  # player 2 wins
                            self.game_over_flag = True
                        else:  # If they have equal length, remove both
                            self.snake1_body = []
                            self.snake2_body = []
                            self.game_over_flag = True
                        return  # Exit the function after a collision is detected

        # Check if the game is over (both snakes are gone)
        if not self.snake1_body and not self.snake2_body:
            self.game_over_flag = True

    def draw_elements(self, colors: Optional[Tuple[Tuple[int, int, int], ...]] = None) -> None:
        super().draw_elements(colors)  # Call the BaseLogic version to draw background and basic border

        if colors is None:
            colors = self.DEFAULT_COLORS
        black, red, magenta, blue, white = colors

        # Draw player 1's snake
        if self.snake1_body:
            for pos in self.snake1_body:
                pygame.draw.rect(self.game_window, blue, pygame.Rect(pos[0], pos[1], self.block_size, self.block_size))

        # Draw player 2's snake
        if self.snake2_body:
            for pos in self.snake2_body:
                pygame.draw.rect(self.game_window, red, pygame.Rect(pos[0], pos[1], self.block_size, self.block_size))

        # Draw the food
        for food in self.food_pos:
            if food:
                pygame.draw.rect(self.game_window, magenta, pygame.Rect(food[0], food[1], self.block_size, self.block_size))

        self.draw_border_and_score() # call the multiplayer version
        pygame.display.update()

    def draw_border_and_score(self) -> None:
        pygame.draw.rect(self.game_window, COLORS["GRAY"], (0, 0, self.window_width, self.border_height))
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SCORE)

        # Player 1 score with name
        score1_surface = font.render(f"{self.player1_name}: {self.score1}", True, COLORS["WHITE"])  # Use score1
        self.game_window.blit(score1_surface, (10, 10))

        # Player 2 score (top right)
        score2_surface = font.render(f"{self.player2_name}: {self.score2}", True, COLORS["WHITE"])  # Use score2
        score2_rect = score2_surface.get_rect()
        score2_rect.topright = (self.window_width - 10, 10)
        self.game_window.blit(score2_surface, score2_rect)

    def game_over(self) -> int:
        """Handles game over logic for multiplayer, displaying winner or tie."""
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SCORE * 2)

        if hasattr(self, 'winner') and self.winner:  # Check if a winner was determined
            if self.winner == 1:
                winner_name = self.player1_name
            elif self.winner == 2:
                winner_name = self.player2_name
            else:
                winner_name = "Someone"  # Handle unexpected winner values

            winner_text = font.render(f"Winner: {winner_name}", True, COLORS["WHITE"])
        else:  # No winner (tie)
            winner_text = font.render("Game Over! (Tie)", True, COLORS["WHITE"])

        winner_rect = winner_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self.game_window.fill(COLORS["BLACK"])  # Clear the screen
        self.game_window.blit(winner_text, winner_rect)
        self.draw_border_and_score()  # Redraw the score
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return 0  # Return 0 to prevent score insertion

