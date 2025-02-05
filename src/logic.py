import pygame
import sys
import time
import random

class GameLogic:
    def __init__(self, game_window, fps_controller, window_width, window_height):
        self.game_window = game_window
        self.fps_controller = fps_controller
        self.window_width = window_width
        self.window_height = window_height
        self.border_height = 50  # Höhe des Score-Bereichs
        self.game_over_flag = False
        self.block_size = 10  # Größe eines Schlangensegments

        # Spielfeldgröße ohne den Score-Bereich
        self.playable_height = self.window_height

        # Berechne den Mittelpunkt des Spielfelds
        center_x = (window_width // 2 // self.block_size) * self.block_size
        center_y = ((self.playable_height // 2 + self.border_height) // self.block_size) * self.block_size

        self.snake_pos = [center_x, center_y]
        self.snake_body = [
            self.snake_pos[:],
            [center_x - self.block_size, center_y],
            [center_x - 2 * self.block_size, center_y]
        ]
        self.food_pos = self.spawn_food()
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
        """Aktualisiert die Position der Schlange und prüft Kollisionen mit den Wänden."""
        if self.direction == "UP":
            self.snake_pos[1] -= self.block_size
        elif self.direction == "DOWN":
            self.snake_pos[1] += self.block_size
        elif self.direction == "LEFT":
            self.snake_pos[0] -= self.block_size
        elif self.direction == "RIGHT":
            self.snake_pos[0] += self.block_size

        #Prüft Kollisionen
        if (self.snake_pos[0] < 0 or self.snake_pos[0] >= self.window_width or
            self.snake_pos[1] < self.border_height or self.snake_pos[1] + self.block_size > self.window_height):
            self.game_over_flag = True

    def update_snake_body(self):
        """Aktualisiert den Schlangenkörper und prüft, ob Essen gefressen wurde."""
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos == self.food_pos:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        if not self.food_spawn:
            self.food_pos = self.spawn_food()
            self.food_spawn = True

    def spawn_food(self):
        """Generiert eine neue Position für das Essen, die nicht im Score-Bereich liegt."""
        while True:
            new_food_pos = [
                random.randrange(0, self.window_width // self.block_size) * self.block_size,
                random.randrange(self.border_height // self.block_size, self.window_height // self.block_size) * self.block_size
            ]
            if new_food_pos not in self.snake_body:  # Stelle sicher, dass das Essen nicht auf der Schlange erscheint
                return new_food_pos

    def check_collisions(self):
        """Prüft, ob die Schlange sich selbst berührt."""
        return any(block == self.snake_pos for block in self.snake_body[1:])

    def draw_elements(self, colors):
        """Zeichnet das Spielfeld, die Schlange und das Essen."""
        black, red, magenta, blue, white = colors

        # Spielfeldhintergrund zeichnen
        self.game_window.fill(black, (0, self.border_height, self.window_width, self.window_height - self.border_height))

        # Schlange zeichnen
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, blue, pygame.Rect(pos[0], pos[1], self.block_size, self.block_size))

        # Essen zeichnen
        pygame.draw.rect(self.game_window, magenta, pygame.Rect(self.food_pos[0], self.food_pos[1], self.block_size, self.block_size))

        # Score-Rand zeichnen
        self.draw_border_and_score()

        pygame.display.update()

    def draw_border_and_score(self):
        """Zeichnet den oberen Randbereich und zeigt den Score dort an."""
        font = pygame.font.SysFont("arial", 30)

        # Score-Hintergrundbereich zeichnen
        pygame.draw.rect(self.game_window, (50, 50, 50), (0, 0, self.window_width, self.border_height))

        # Score-Anzeige
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.game_window.blit(score_text, (self.window_width // 2 - score_text.get_width() // 2, 10))

    def game_over(self, colors=None):
        """Zeigt den Game Over Screen an und gibt den finalen Score zurück."""
        if colors is None or len(colors) < 5:
            colors = ((0, 0, 0), (255, 0, 0), (255, 6, 254), (0, 255, 255), (255, 255, 255))
        black, red, magenta, blue, white = colors
        font = pygame.font.SysFont("arial", 50)
        game_over_surface = font.render('Game Over', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_width // 2, self.window_height // 4)
        self.game_window.fill(black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.draw_border_and_score()
        pygame.display.flip()
        time.sleep(3)
        return self.score
