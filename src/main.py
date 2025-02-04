# main.py
import pygame
import sys
from logic import GameLogic
from db_score import DBScore

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


def get_player_name(game_window, fps_controller):
    """Zeigt ein Eingabefeld zur Namenseingabe an und gibt den eingegebenen Namen zurück."""
    font = pygame.font.SysFont("arial", 30)
    input_box = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
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
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        game_window.fill((0, 0, 0))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        game_window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(game_window, color, input_box, 2)
        instruction = font.render("Name eingeben", True, pygame.Color('white'))
        game_window.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, input_box.y - 40))
        pygame.display.flip()
        fps_controller.tick(40)
    return text


def show_highscore(game_window, fps_controller, db):
    """Zeigt die Top 10 Highscores an."""
    scores = db.get_top_scores()
    font_title = pygame.font.SysFont("arial", 40)
    font_item = pygame.font.SysFont("arial", 30)
    game_window.fill((0, 0, 0))
    title = font_title.render("Highscores", True, (255, 255, 255))
    game_window.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
    y = 120
    if scores:
        for i, (player, score_val, achieved_at) in enumerate(scores, start=1):
            date_str = str(achieved_at)
            text = f"{i}. {player} - {score_val} ({date_str})"
            text_surface = font_item.render(text, True, (255, 255, 255))
            game_window.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, y))
            y += 40
    else:
        no_score = font_item.render("Keine Scores vorhanden", True, (255, 255, 255))
        game_window.blit(no_score, (WINDOW_WIDTH // 2 - no_score.get_width() // 2, y))
    instruction = font_item.render("Taste drücken", True, (255, 255, 255))
    game_window.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, y + 60))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
        fps_controller.tick(30)


def show_menu(game_window, fps_controller, db):
    """Zeigt das Hauptmenü mit den Optionen 'Starten' und 'Highscore' an."""
    font_title = pygame.font.SysFont("arial", 50)
    font_option = pygame.font.SysFont("arial", 30)
    while True:
        game_window.fill((0, 0, 0))
        title_surface = font_title.render("Snake Game", True, (255, 255, 255))
        option1 = font_option.render("1. Starten", True, (255, 255, 255))
        option2 = font_option.render("2. Highscore", True, (255, 255, 255))
        game_window.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 100))
        game_window.blit(option1, (WINDOW_WIDTH // 2 - option1.get_width() // 2, 200))
        game_window.blit(option2, (WINDOW_WIDTH // 2 - option2.get_width() // 2, 250))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start"
                elif event.key == pygame.K_2:
                    show_highscore(game_window, fps_controller, db)
        fps_controller.tick(30)


def main():
    pygame.init()
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    fps_controller = pygame.time.Clock()

    colors = ((0, 0, 0),
              (255, 0, 0),
              (255, 6, 254),
              (0, 255, 255),
              (255, 255, 255))

    # DBScore-Instanz erstellen – passe hier deine DB-Zugangsdaten an!
    db = DBScore(host="localhost", user="alex", password="password", database="gamescore")

    while True:
        selection = show_menu(game_window, fps_controller, db)
        if selection == "start":
            game = GameLogic(game_window, fps_controller, WINDOW_WIDTH, WINDOW_HEIGHT)
            while True:
                game.process_events()
                game.update_direction()
                game.update_snake_position()
                # Prüfe, ob die Schlange den Rand verlassen hat
                if game.game_over_flag:
                    final_score = game.game_over(colors)
                    player_name = get_player_name(game_window, fps_controller)
                    db.insert_score(player_name, final_score)
                    break
                game.update_snake_body()
                if game.check_collisions():
                    final_score = game.game_over(colors)
                    player_name = get_player_name(game_window, fps_controller)
                    db.insert_score(player_name, final_score)
                    break
                game.draw_elements(colors)
                fps_controller.tick(20)


if __name__ == '__main__':
    main()
