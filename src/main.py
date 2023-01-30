import sys
import time

import pygame
from pygame.locals import *

from src.components.game_status import GameStatus
from src.components.hand import Hand
from src.components.hand_side import HandSide
from src.components.player import Player
from src.components.scoreboard import Scoreboard
from src.config import Config
from src.global_state import GlobalState
from src.services.music_service import MusicService
from src.services.visualization_service import VisualizationService

pygame.init()

GlobalState.load_main_screen()
VisualizationService.load_main_game_displays()

scoreboard = Scoreboard()

FramePerSec = pygame.time.Clock()

# Menu
press_y = 650
curtain_y = -1300


def update_background_using_scroll(scroll):
    scroll -= .5

    if scroll < -80:
        scroll = 0

    VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, scroll)

    return scroll


def update_press_key(press_y):
    if press_y > 460:
        return press_y * 0.99

    return press_y


def game_over():
    GlobalState.GAME_STATE = GameStatus.MAIN_MENU
    time.sleep(0.5)


# Sprite Setup
P1 = Player()
H1 = Hand(HandSide.RIGHT)
H2 = Hand(HandSide.LEFT)

# Sprite Groups
hands = pygame.sprite.Group()
hands.add(H1)
hands.add(H2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(H1)
all_sprites.add(H2)


def gameplay_phase():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    P1.update()

    GlobalState.PLAYER_POSITION = P1.player_position.copy()
    H1.move(scoreboard, GlobalState.PLAYER_POSITION)
    H2.move(scoreboard, GlobalState.PLAYER_POSITION)

    GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)

    P1.draw(GlobalState.SCREEN)
    H1.draw(GlobalState.SCREEN)
    H2.draw(GlobalState.SCREEN)
    scoreboard.draw(GlobalState.SCREEN)

    if pygame.sprite.spritecollide(P1, hands, False, pygame.sprite.collide_mask):
        scoreboard.update_max_score()

        MusicService.play_slap_sound()
        time.sleep(0.5)

        P1.reset()
        H1.reset()
        H2.reset()
        game_over()


def update_game_display():
    pygame.display.update()
    FramePerSec.tick(Config.FPS)


def close_app():
    pygame.quit()
    sys.exit()


def main_menu_phase():
    global press_y

    for event in pygame.event.get():
        if event.type == QUIT:
            GlobalState.GAME_STATE = GameStatus.GAME_END
            return

        if event.type == pygame.KEYDOWN:
            GlobalState.GAME_STATE = GameStatus.GAMEPLAY
            return

    GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)

    press_y = update_press_key(press_y)

    VisualizationService.draw_main_menu(GlobalState.SCREEN, scoreboard.get_max_score(), press_y)


def main():
    while True:
        if GlobalState.GAME_STATE == GameStatus.MAIN_MENU:
            scoreboard.reset_current_score()
            main_menu_phase()
        elif GlobalState.GAME_STATE == GameStatus.GAMEPLAY:
            gameplay_phase()
        elif GlobalState.GAME_STATE == GameStatus.GAME_END:
            close_app()

        MusicService.start_background_music()
        update_game_display()


if __name__ == "__main__":
    main()
