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
}

FONT_NAME = "arial"
FONT_SIZE_SCORE = 30
FONT_SIZE_GAME_OVER = 50


class GameLogic:
    def __init__(self, game_window: pygame.Surface, fps_controller: pygame.time.Clock, window_width: int, window_height: int):
        """
        Initialisiert die Spiel-Logik.

        :param game_window: Das Pygame-Fenster, auf dem gezeichnet wird.
        :param fps_controller: Der Pygame-FPS-Controller.
        :param window_width: Die Breite des Fensters.
        :param window_height: Die Höhe des Fensters.
        """
        self.game_window = game_window
        self.fps_controller = fps_controller
        self.window_width = window_width
        self.window_height = window_height
        self.border_height = 50  # Höhe des Score-Bereichs
        self.game_over_flag = False
        self.block_size = 10  # Größe eines Schlangensegments

        # Spielfeldgröße ohne den Score-Bereich
        self.playable_height = self.window_height - self.border_height

        # Berechne den Mittelpunkt des Spielfelds
        center_x = (window_width // 2 // self.block_size) * self.block_size
        center_y = ((self.playable_height // 2) // self.block_size) * self.block_size + self.border_height

        # Initialisiere die Schlange und das Essen
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

    def process_events(self) -> None:
        """
        Verarbeitet Tastatur- und Fenster-Events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """
        Verarbeitet Tastendrücke und aktualisiert die Richtung der Schlange.

        :param event: Das Pygame-Event-Objekt.
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
        Aktualisiert die aktuelle Richtung (keine 180°-Drehung).
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
        Aktualisiert die Position der Schlange und prüft Kollisionen mit den Wänden.
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
        Aktualisiert den Schlangenkörper und prüft, ob Essen gefressen wurde.
        """
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos == self.food_pos:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        if not self.food_spawn:
            self.food_pos = self.spawn_food()
            self.food_spawn = True

    def spawn_food(self) -> List[int]:
        """
        Generiert eine neue Position für das Essen, die nicht im Score-Bereich liegt.

        :return: Die Position des Essens als Liste [x, y].
        """
        while True:
            new_food_pos = [
                random.randrange(0, self.window_width // self.block_size) * self.block_size,
                random.randrange(self.border_height // self.block_size,
                                 self.window_height // self.block_size) * self.block_size
            ]
            if new_food_pos not in self.snake_body:
                return new_food_pos

    def check_collisions(self) -> bool:
        """
        Prüft, ob die Schlange sich selbst berührt.

        :return: True, wenn eine Kollision vorliegt, sonst False.
        """
        if (self.snake_pos[0] < 0 or  # Left boundary
                self.snake_pos[0] >= self.window_width or  # Right boundary
                self.snake_pos[1] < self.border_height or  # Top boundary (after border)
                self.snake_pos[1] >= self.window_height):  # Bottom boundary
            return True

        if self.snake_pos in self.snake_body[1:]:
            return True

        return False

    def draw_elements(self, colors: Optional[Tuple[Tuple[int, int, int], ...]] = None) -> None:
        """
        Zeichnet das Spielfeld, die Schlange und das Essen.

        :param colors: Ein optionales Tupel mit Farben für das Spielfeld.
        """
        if colors is None or len(colors) < 5:
            colors = (
                COLORS["BLACK"], COLORS["RED"], COLORS["MAGENTA"], COLORS["BLUE"], COLORS["WHITE"]
            )
        black, red, magenta, blue, white = colors

        # Spielfeldhintergrund zeichnen ohne Score
        self.game_window.fill(black, (0, self.border_height, self.window_width, self.playable_height))

        # Schlange zeichnen
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, blue, pygame.Rect(pos[0], pos[1], self.block_size, self.block_size))

        # Essen zeichnen
        pygame.draw.rect(self.game_window, magenta, pygame.Rect(self.food_pos[0], self.food_pos[1], self.block_size, self.block_size))

        # Score-Bereich und Score anzeigen
        self.draw_border_and_score()

        pygame.display.update()

    def draw_border_and_score(self) -> None:
        """
        Zeichnet den Score-Bereich und zeigt den Score dort an.
        """
        # Score-Hintergrundbereich zeichnen
        pygame.draw.rect(self.game_window, COLORS["GRAY"], (0, 0, self.window_width, self.border_height))

        # Score-Anzeige
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SCORE)
        score_surface = font.render(f"Score: {self.score}", True, COLORS["WHITE"])
        self.game_window.blit(score_surface, (10, 10))

    def game_over(self, colors: Optional[Tuple[Tuple[int, int, int], ...]] = None) -> int:
        """
        Zeigt den Game Over Screen an und gibt den finalen Score zurück.

        :param colors: Ein optionales Tupel mit Farben für den Game Over Screen.
        :return: Der finale Score.
        """
        if colors is None or len(colors) < 5:
            colors = (
                COLORS["BLACK"], COLORS["RED"], COLORS["MAGENTA"], COLORS["BLUE"], COLORS["WHITE"]
            )
        black, red, magenta, blue, white = colors

        try:
            font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_GAME_OVER)
        except pygame.error as err:
            print(f"Fehler beim Laden der Schriftart: {err}")
            return self.score

        game_over_surface = font.render('Game Over', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_width // 2, self.window_height // 4)
        self.game_window.fill(black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.draw_border_and_score()
        pygame.display.flip()
        time.sleep(1)
        return self.score