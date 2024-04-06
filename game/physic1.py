import pygame
pygame.init()
WIDTH, HEIGHT = (700, 950)
GRAVITY = 400  # Ускорение свободного падения
N = 9  # Множитель для увеличения высоты начального прыжка
X = 7  # Скорость движения влево и вправо
FPS = 60
DT = FPS / 1000.0
class Player:
    def __init__(self, x, y) -> None:
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = (x, y)
        self.dx = 0
        self.jump_power = 20
        self.velocity_y = 0
        self.on_ground = True  # Переменная, чтобы проверить, на земле ли игрок

    def move(self):
        keys = pygame.key.get_pressed()
        if self.on_ground and not keys[pygame.K_SPACE]: # Если игрок на земле и не заряжает прыжок
            if keys[pygame.K_LEFT]:
                self.dx = -X # Двигаемся влево
            elif keys[pygame.K_RIGHT]:
                self.dx = X # Двигаемся вправо
            else:
                self.dx = 0 # Стоим на месте
            self.rect.x += self.dx

    def border_collision(self):
        if (self.rect.x < 0):
            self.rect.x = 0
            self.dx = -self.dx
        if (self.rect.x > WIDTH - 50):
            self.rect.x = WIDTH - 50
            self.dx = -self.dx # отскок от стен
        if self.rect.y > HEIGHT - 50:
            self.rect.y = HEIGHT - 50
            self.on_ground = True  # Устанавливаем, что игрок на земле

    def jump_charge(self):
        key = pygame.key.get_pressed()
        if self.on_ground:
            if key[pygame.K_SPACE]:  # Зарядка прыжка возможна только на земле
                self.jump_power += 1
                self.jump_power = min(self.jump_power, 100)
            if key[pygame.K_LEFT]: # Если игрок заряжает прыжок и нажимает налево
                self.dx = -X
            if key[pygame.K_RIGHT]: # Если игрок заряжает прыжок и нажимает направо
                self.dx = X

    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_power*N # Прыгаем с силой, равной заряду, помноженному на N, чтобы увеличить высоту начального прыжка
            self.on_ground = False
            self.jump_power = 20

    def update(self):
        if not self.on_ground:
            self.velocity_y += GRAVITY * DT
            self.rect.y += self.velocity_y * DT / 2
            self.rect.x += self.dx # Двигаемся влево или вправо (константа) во время прыжка
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.on_ground = True
                self.velocity_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
player = Player(350, 975)
done = 0

while not done:
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
    player.update()  # Вызываем обновление игрока с dt
    player.border_collision()

    # debug
    screen.blit(pygame.font.Font(None, 18).render(f"POS: {player.rect.x}, {player.rect.y}", True, (255, 255, 255)), (10,10))
    screen.blit(pygame.font.Font(None, 18).render(f"Holding power: {player.jump_power}", True, (255, 255, 255)), (10,30))
    screen.blit(pygame.font.Font(None, 18).render(f"Dx: {player.dx}", True, (255, 255, 255)), (10,50))
    screen.blit(pygame.font.Font(None, 18).render(f"Velocity: {player.velocity_y}", True, (255, 255, 255)), (10,70))
    pygame.time.Clock().tick(FPS)
    pygame.display.flip()