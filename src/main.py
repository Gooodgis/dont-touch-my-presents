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
from src.utils.tools import update_background_using_scroll, update_press_key

FramePerSec = pygame.time.Clock()

pygame.init()

GlobalState.load_main_screen()
VisualizationService.load_main_game_displays()

scoreboard = Scoreboard()

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


def game_over():
    P1.reset()
    H1.reset()
    H2.reset()
    GlobalState.GAME_STATE = GameStatus.MAIN_MENU
    time.sleep(0.5)


def update_game_display():
    pygame.display.update()
    FramePerSec.tick(Config.FPS)


def close_app():
    pygame.quit()
    sys.exit()


def gameplay_phase():
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            game_over()

    P1.update()
    H1.move(scoreboard, P1.player_position)
    H2.move(scoreboard, P1.player_position)

    GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
    VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)

    P1.draw(GlobalState.SCREEN)
    H1.draw(GlobalState.SCREEN)
    H2.draw(GlobalState.SCREEN)
    scoreboard.draw(GlobalState.SCREEN)

    if pygame.sprite.spritecollide(P1, hands, False, pygame.sprite.collide_mask):
        scoreboard.update_max_score()
        MusicService.play_slap_sound()
        time.sleep(0.5)
        game_over()


def main_menu_phase():
    events = pygame.event.get()

    for event in events:
        if event.type != pygame.KEYDOWN:
            continue

        if event.key == K_ESCAPE:
            GlobalState.GAME_STATE = GameStatus.GAME_END
            return

        GlobalState.GAME_STATE = GameStatus.GAMEPLAY

        pygame.event.clear()

    GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
    VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)
    GlobalState.PRESS_Y = update_press_key(GlobalState.PRESS_Y)
    VisualizationService.draw_main_menu(GlobalState.SCREEN, scoreboard.get_max_score(), GlobalState.PRESS_Y)


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
