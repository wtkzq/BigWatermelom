import game
from settings import settings
import logging

logging.basicConfig(format="%(levelname)s (file %(filename)s, in %(funcName)s, line %(lineno)s, %(asctime)s): %("
                           "message)s", level=logging.INFO)
game.Game(settings).main_loop()
