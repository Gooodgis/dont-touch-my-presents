import pygame


from src.components.game_status import GameStatus
from src.config import Config
from src.game_phases import main_menu_phase, gameplay_phase, exit_game_phase
from src.global_state import GlobalState
from src.services.music_service import MusicService

# executable making
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

asset_url = resource_path("data/assets/gift.png")
gift = pygame.image.load(asset_url)
# executable making

pygame.init()

FramePerSec = pygame.time.Clock()

def update_game_display():
    pygame.display.update()
    FramePerSec.tick(Config.FPS)


def main():
    while True:
        if GlobalState.GAME_STATE == GameStatus.MAIN_MENU:
            main_menu_phase()
        elif GlobalState.GAME_STATE == GameStatus.GAMEPLAY:
            gameplay_phase()
        elif GlobalState.GAME_STATE == GameStatus.GAME_END:
            exit_game_phase()

        MusicService.start_background_music()
        update_game_display()


if __name__ == "__main__":
    main()
