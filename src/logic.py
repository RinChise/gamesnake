# logic.py
import pygame
import sys
import time
import random

class GameLogic:
    def __init__(self, game_window, fps_controller, width, height):
        self.game_window = game_window
        self.fps_controller = fps_controller
        self.window_width = width
        self.window_height = height
        self.game_over_flag = False
        self.block_size = 10  # Größe eines Schlangensegments

        # Berechne den Mittelpunkt des Fensters (auf ein Vielfaches von block_size gerundet)
        center_x = (width // 2 // self.block_size) * self.block_size
        center_y = (height // 2 // self.block_size) * self.block_size

        self.snake_pos = [center_x, center_y]
        self.snake_body = [
            self.snake_pos[:],
            [center_x - self.block_size, center_y],
            [center_x - 2 * self.block_size, center_y]
        ]
        self.food_pos = [
            random.randrange(1, (width // self.block_size)) * self.block_size,
            random.randrange(1, (height // self.block_size)) * self.block_size
        ]
        self.food_spawn = True
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.score = 0

    def process_events(self):
        """Verarbeitet Tastatur- und Fenster-Events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.change_to = "UP"
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.change_to = "DOWN"
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.change_to = "LEFT"
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.change_to = "RIGHT"

    def update_direction(self):
        """Aktualisiert die aktuelle Richtung (keine 180°-Drehung)."""
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def update_snake_position(self):
        """Aktualisiert die Position der Schlange und prüft, ob sie den Fensterrand verlässt."""
        if self.direction == "UP":
            self.snake_pos[1] -= self.block_size
        elif self.direction == "DOWN":
            self.snake_pos[1] += self.block_size
        elif self.direction == "LEFT":
            self.snake_pos[0] -= self.block_size
        elif self.direction == "RIGHT":
            self.snake_pos[0] += self.block_size

        """
        # Wrap-Around Logik: Schlange erscheint am anderen Rand
        if self.snake_pos[0] < 0:
            self.snake_pos[0] = self.window_width - 10
        elif self.snake_pos[0] > self.window_width - 10:
            self.snake_pos[0] = 0

        if self.snake_pos[1] < 0:
            self.snake_pos[1] = self.window_height - 10
        elif self.snake_pos[1] > self.window_height - 10:
            self.snake_pos[1] = 0
        """
        # Rand-Check: Verläßt die Schlange den Spielfensterbereich, dann Game Over
        if (self.snake_pos[0] < 0 or self.snake_pos[0] >= self.window_width or
            self.snake_pos[1] < 0 or self.snake_pos[1] >= self.window_height):
            self.game_over_flag = True

    def update_snake_body(self):
        """Aktualisiert den Schlangenkörper und prüft, ob Essen gefressen wurde."""
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        if not self.food_spawn:
            self.food_pos = [
                random.randrange(1, (self.window_width // self.block_size)) * self.block_size,
                random.randrange(1, (self.window_height // self.block_size)) * self.block_size
            ]
            self.food_spawn = True

    def check_collisions(self):
        """Prüft, ob die Schlange sich selbst berührt."""
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return True
        return False

    def draw_elements(self, colors):
        """Zeichnet Schlange, Essen und Score auf dem Spielfenster."""
        black, red, magenta, blue, white = colors
        self.game_window.fill(black)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, blue,
                             pygame.Rect(pos[0], pos[1], self.block_size, self.block_size))
        pygame.draw.rect(self.game_window, magenta,
                         pygame.Rect(self.food_pos[0], self.food_pos[1], self.block_size, self.block_size))
        self.show_score(white, "arial", 20)
        pygame.display.update()

    def show_score(self, color, font_name, size):
        """Zeigt den aktuellen Score an."""
        font = pygame.font.SysFont(font_name, size)
        score_surface = font.render('Score: ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.window_width // 10, 15)
        self.game_window.blit(score_surface, score_rect)

    def game_over(self, colors=None):
        """Zeigt den Game Over Screen an und gibt den finalen Score zurück."""
        if colors is None:
            colors = ((0, 0, 0), (255, 0, 0), (0, 255, 255), (255, 255, 255))
        black, red, magenta, blue, white = colors
        font = pygame.font.SysFont("arial", 50)
        game_over_surface = font.render('Game Over', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_width // 2, self.window_height // 4)
        self.game_window.fill(black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.show_score(white, "Arial", 20)
        pygame.display.flip()
        time.sleep(3)
        return self.score
