import pygame
pygame.init()
WIDTH, HEIGHT = (700, 1000)
GRAVITY = 500  # Ускорение свободного падения
FPS = 60

class Player:
    def __init__(self, x, y) -> None:
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = (x, y)
        self.jump_power = 0
        self.velocity_y = 0
        self.on_ground = True  # Переменная, чтобы проверить, на земле ли игрок

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10

    def border_collision(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - 50:
            self.rect.x = WIDTH - 50
        if self.rect.y > HEIGHT - 50:
            self.rect.y = HEIGHT - 50
            self.on_ground = True  # Устанавливаем, что игрок на земле

    def jump_charge(self):
        key = pygame.key.get_pressed()
        if self.on_ground and key[pygame.K_SPACE]:  # Зарядка прыжка возможна только на земле
            self.jump_power += 1
            self.jump_power = min(self.jump_power, 100)

    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_power*4 # Прыгаем с силой, равной заряду, помноженному на N, чтобы увеличить высоту прыжка
            self.on_ground = False
            self.jump_power = 0

    def update(self, dt):
        if not self.on_ground:
            self.velocity_y += GRAVITY * dt
            self.rect.y += self.velocity_y * dt
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.on_ground = True
                self.velocity_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

player = Player(350, 975)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
done = 0

while not done:
    dt = clock.tick(FPS) / 1000.0  # Delta time в секундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.jump()  # Запускаем прыжок

    screen.fill((0, 0, 0))
    player.draw(screen)
    player.jump_charge()
    player.move()
    player.update(dt)  # Вызываем обновление игрока с dt
    player.border_collision()

    screen.blit(pygame.font.Font(None, 18).render(f"{player.rect.x}, {player.rect.y}", True, (255, 255, 255)), (10,10))
    screen.blit(pygame.font.Font(None, 18).render(f"{player.jump_power}", True, (255, 255, 255)), (10,30))
    pygame.display.flip()