import pygame
import sys
from typing import Optional, List, Tuple
from logic import BaseLogic
from singleplayer import SingleplayerLogic
from db_score import DBScore

# Konstanten für Fenstergröße und Farben
WINDOW_WIDTH = 800
BORDER_HEIGHT = 50
GAME_HEIGHT = 800
WINDOW_HEIGHT = GAME_HEIGHT + BORDER_HEIGHT

COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "LIGHT_SKY_BLUE": (135, 206, 250),
    "DODGER_BLUE": (30, 144, 255),
}

FONT_NAME = "arial"
FONT_SIZE_TITLE = 50
FONT_SIZE_OPTION = 30
FONT_SIZE_INPUT = 30


def get_player_name(game_window: pygame.Surface, fps_controller: pygame.time.Clock, window_width: int) -> str:
    """
    Zeigt ein Eingabefeld zur Namenseingabe an und gibt den eingegebenen Namen zurück.

    :param game_window: Das Pygame-Fenster, auf dem gezeichnet wird.
    :param fps_controller: Der Pygame-FPS-Controller.
    :param window_width: Die Breite des Fensters.
    :return: Der eingegebene Name als String.
    """
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_INPUT)
    input_box = pygame.Rect(window_width // 2 - 100, 400, 200, 40)
    color_inactive = COLORS["LIGHT_SKY_BLUE"]
    color_active = COLORS["DODGER_BLUE"]
    color = color_inactive
    active = False
    text = ""
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    if text.strip():  # Leere Eingaben verhindern
                        done = True
                    else:
                        print("⚠ Kein Name eingegeben, bitte etwas eingeben!")
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        game_window.fill(COLORS["BLACK"])

        txt_surface = font.render(text, True, color)
        input_box.w = max(200, txt_surface.get_width() + 10)
        game_window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(game_window, color, input_box, 2)

        instruction = font.render("Gib deinen Namen ein:", True, COLORS["WHITE"])
        game_window.blit(instruction, (window_width // 2 - instruction.get_width() // 2, input_box.y - 40))

        pygame.display.flip()
        fps_controller.tick(30)

    return text.strip()  # Entfernt ungewollte Leerzeichen


def show_highscore(game_window: pygame.Surface, fps_controller: pygame.time.Clock, db: DBScore) -> None:
    """
    Zeigt die Top 10 Highscores an.

    :param game_window: Das Pygame-Fenster, auf dem gezeichnet wird.
    :param fps_controller: Der Pygame-FPS-Controller.
    :param db: Die Datenbankverbindung für die Highscores.
    """
    scores = db.get_top_scores()
    font_title = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TITLE)
    font_item = pygame.font.SysFont(FONT_NAME, FONT_SIZE_OPTION)
    game_window.fill(COLORS["BLACK"])
    title = font_title.render("Highscore", True, COLORS["WHITE"])
    game_window.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
    y = 120
    if scores:
        for i, (player, score_val, achieved_at) in enumerate(scores, start=1):
            text_surface = font_item.render(f"{i}. {player} - {score_val} ({achieved_at})", True, COLORS["WHITE"])
            game_window.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, y))
            y += 40
    else:
        no_score = font_item.render("Keine Scores vorhanden", True, COLORS["WHITE"])
        game_window.blit(no_score, (WINDOW_WIDTH // 2 - no_score.get_width() // 2, y))
    instruction = font_item.render("Taste drücken", True, COLORS["WHITE"])
    game_window.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, y + 60))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        fps_controller.tick(30)


def show_menu(game_window: pygame.Surface, fps_controller: pygame.time.Clock, db: DBScore) -> str:
    """
    Zeigt das Hauptmenü mit den Optionen an.

    :param game_window: Das Pygame-Fenster, auf dem gezeichnet wird.
    :param fps_controller: Der Pygame-FPS-Controller.
    :param db: Die Datenbankverbindung für die Highscores.
    :return: Die ausgewählte Option als String.
    """
    font_title = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TITLE)
    font_option = pygame.font.SysFont(FONT_NAME, FONT_SIZE_OPTION)
    while True:
        game_window.fill(COLORS["BLACK"])
        title_surface = font_title.render("Snake Game", True, COLORS["WHITE"])
        option1 = font_option.render("1. Singleplayer", True, COLORS["WHITE"])
        option2 = font_option.render("2. Multiplayer", True, COLORS["WHITE"])
        option3 = font_option.render("3. Highscore", True, COLORS["WHITE"])
        option4 = font_option.render("4. Beenden", True, COLORS["WHITE"])
        game_window.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 100))
        game_window.blit(option1, (WINDOW_WIDTH // 2 - option1.get_width() // 2, 200))
        game_window.blit(option2, (WINDOW_WIDTH // 2 - option2.get_width() // 2, 250))
        game_window.blit(option3, (WINDOW_WIDTH // 2 - option3.get_width() // 2, 300))
        game_window.blit(option4, (WINDOW_WIDTH // 2 - option4.get_width() // 2, 350))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "singleplayer"
                elif event.key == pygame.K_2:
                    return "multiplayer"
                elif event.key == pygame.K_3:
                    show_highscore(game_window, fps_controller, db)
                elif event.key == pygame.K_4:
                    sys.exit()
        fps_controller.tick(30)


def main() -> None:
    """
    Hauptfunktion des Spiels. Initialisiert Pygame und startet das Spiel.
    """
    pygame.init()
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    fps_controller = pygame.time.Clock()
    db = DBScore()

    while True:
        selection = show_menu(game_window, fps_controller, db)
        if selection == "singleplayer":
            game = SingleplayerLogic(game_window, fps_controller, WINDOW_WIDTH, WINDOW_HEIGHT)

            while True:
                game.process_events()
                game.update_direction()
                game.update_snake_position()

                if game.game_over_flag or game.check_collisions():
                    final_score = game.game_over()

                    if final_score > 0:
                        player_name = get_player_name(game_window, fps_controller, WINDOW_WIDTH)
                        db.insert_score(player_name, final_score)

                    break
                game.update_snake_body()
                game.draw_elements()
                pygame.display.flip()
                fps_controller.tick(30)

        if selection == "multiplayer":
            pass


if __name__ == '__main__':
    main()