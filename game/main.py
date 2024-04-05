import pygame
from sympy import cos, sin, pi

WIDTH, HEIGHT = (700, 1000)


class Player:
    def __init__(self) -> None:
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT-self.image.get_size()[1]
    def draw(self, screen):
        pass

class Level():
    def __init__(self, bg_image, collisions_dict) -> None:
        pass
    def change_level(self):
        pass
    def draw(self, screen):
        pass


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player = Player()
        self.current_level = Level()
        self.done = 0

    def run(self):
        while 1:
            self.handle_events()
            if not self.done:
                self.update()
                self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = 1

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        
if __name__ == "__main__":
    game = Game()
    game.run()