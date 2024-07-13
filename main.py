import sys
import pygame
from pygame.locals import *


class App:
    def __init__(self):
        self.screen_size = self.screen_width, self.screen_height = 800, 600
        self.screen = None
        self.running = True

        self.FPS = 60

        self.clock = None

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Race')

        self.clock = pygame.time.Clock()

        return True

    def on_execute(self):
        if not self.on_init():
            self.running = False

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

            self.clock.tick(self.FPS)

        self.on_cleanup()

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    app = App()
    app.on_execute()
