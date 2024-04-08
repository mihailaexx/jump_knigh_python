import pygame
pygame.init()

WIDTH, HEIGHT = (700, 950)
GRAVITY = 400
JUMP_POWER_MULIPLYER = 9
DX = 7
FPS = 60
DT = FPS / 1000.0

class Player:
    def __init__(self, x, y) -> None:
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = (x, y)
        self.dx = 0
        self.jump_power = 20
        self.velocity_y = 0
        self.on_ground = False

    def move(self):
        keys = pygame.key.get_pressed()
        if self.on_ground and not keys[pygame.K_SPACE]:
            if keys[pygame.K_LEFT]:
                self.dx = -DX
            elif keys[pygame.K_RIGHT]:
                self.dx = DX
            else:
                self.dx = 0
            self.rect.x += self.dx

    def border_collision(self, levels):
        for block in levels.list[levels.current_level_index]:
            if self.rect.colliderect(block.rect):
                distances = {
                    'top': abs(self.rect.bottom - block.rect.top),
                    'bottom': abs(self.rect.top - block.rect.bottom),
                    'left': abs(self.rect.right - block.rect.left),
                    'right': abs(self.rect.left - block.rect.right)
                }

                min_distance = min(distances, key=distances.get)
                
                if min_distance == 'top' and self.velocity_y > 0:
                    self.rect.bottom = block.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    break
                elif min_distance == 'bottom' and self.velocity_y < 0:
                    self.rect.top = block.rect.bottom
                    self.velocity_y = 0
                elif min_distance == 'left' and self.dx > 0:
                    self.rect.right = block.rect.left
                    self.dx = -self.dx
                elif min_distance == 'right' and self.dx < 0:
                    self.rect.left = block.rect.right
                    self.dx = -self.dx
            elif not self.rect.colliderect(block.rect) and self.rect.y < HEIGHT - 50:
                self.on_ground = False
        if (self.rect.x < 0):
            self.rect.x = 0
            self.dx = -self.dx
        if (self.rect.x > WIDTH - 50):
            self.rect.x = WIDTH - 50
            self.dx = -self.dx
        if self.rect.y < 0:
            self.rect.y = HEIGHT - 50
            levels.current_level_index += 1
        if self.rect.y > HEIGHT - 50:
            if levels.current_level_index == 0:
                self.rect.y = HEIGHT - 50
                self.velocity_y = 0
                self.on_ground = True
            else:
                self.rect.y = 0
                levels.current_level_index -= 1

    def jump_charge(self):
        key = pygame.key.get_pressed()
        if self.on_ground:
            if key[pygame.K_SPACE]:
                self.jump_power += 1
                self.jump_power = min(self.jump_power, 100)
            if key[pygame.K_LEFT]:
                self.dx = -DX
            if key[pygame.K_RIGHT]:
                self.dx = DX

    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_power*JUMP_POWER_MULIPLYER
            self.on_ground = False
            self.jump_power = 20

    def update(self):
        if not self.on_ground:
            self.velocity_y += GRAVITY * DT
            self.rect.y += self.velocity_y * DT / 2
            self.rect.x += self.dx

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Block:
    def __init__(self, x, y, lenght, height) -> None:
        self.posx = x
        self.posy = y
        self.lenght = lenght
        self.height = height
        self.rect = pygame.Rect(x, y, lenght, height)
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

class Levels():
    def __init__(self) -> None:
        self.list = [
            [Block(0,HEIGHT, WIDTH, 1), Block(0, HEIGHT-150, 200, 150), Block(500, HEIGHT-150, 200, 150), Block(200, HEIGHT-625, 300, 150)],
            [],
            []
        ]
        self.current_level_index = 0
    def current_level(self):
        return self.list[self.current_level_index]
    def change_level(self):
        pass
    def draw_level(self, screen):
        for block in self.current_level():
            block.draw(screen)


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player = Player(350, 975)
        self.levels = Levels()
        self.current_level = self.levels.current_level()
        self.done = 0

    def run(self):
        while not self.done:
            self.handle_events()
            self.draw()
            self.update()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self):
        self.player.move()
        self.player.border_collision(self.levels)
        self.player.jump_charge()
        self.player.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        self.levels.draw_level(self.screen)
        self.screen.blit(pygame.font.Font(None, 18).render(f"POS: {self.player.rect.x}, {self.player.rect.y}", True, (255, 255, 255)), (10,10))
        self.screen.blit(pygame.font.Font(None, 18).render(f"Holding power: {self.player.jump_power}", True, (255, 255, 255)), (10,30))
        self.screen.blit(pygame.font.Font(None, 18).render(f"Dx: {self.player.dx}", True, (255, 255, 255)), (10,50))
        self.screen.blit(pygame.font.Font(None, 18).render(f"Velocity: {-self.player.velocity_y}", True, (255, 255, 255)), (10,70))
        self.screen.blit(pygame.font.Font(None, 18).render(f"Level: {self.levels.current_level_index}", True, (255, 255, 255)), (10,90))
        self.screen.blit(pygame.font.Font(None, 18).render(f"On ground: {self.player.on_ground}", True, (255, 255, 255)), (10,110))
        
if __name__ == "__main__":
    game = Game()
    game.run()