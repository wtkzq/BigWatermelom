import game
from settings import settings
import logging


logging.basicConfig(level=logging.INFO)
game.Game(settings).main_loop()
