"""pygbag用程序入口"""
import asyncio
import game
from settings import settings
import pygame


async def main():
    g = game.Game(settings)
    while True:
        g.do_events()
        g.check_lose()
        g.fruit_preview_rect.centerx = pygame.mouse.get_pos()[0]
        g.space.step(1 / g.settings.fps)
        g.draw()
        await asyncio.sleep(0)
        g.clock.tick(g.settings.fps)

asyncio.run(main())
