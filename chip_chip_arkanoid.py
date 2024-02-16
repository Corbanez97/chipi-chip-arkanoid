import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Get screen resolution
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

# Game constants
PADDLE_WIDTH, PADDLE_HEIGHT = 60, 10
BALL_DIMENSION = 2
PADDLE_SPEED = 10
BALL_SPEED = 3
BLOCK_WIDTH, BLOCK_HEIGHT = 3, 3

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Paddle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - PADDLE_HEIGHT - 10
        self.rect = pygame.Rect(int(self.x), self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= speed
        if keys[pygame.K_RIGHT]:
            self.x += speed
        self.rect = pygame.Rect(int(self.x), self.y, PADDLE_WIDTH, PADDLE_HEIGHT)


class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED
        self.rect = pygame.Rect(
            int(self.x), int(self.y), BALL_DIMENSION, BALL_DIMENSION
        )

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect = pygame.Rect(
            int(self.x), int(self.y), BALL_DIMENSION, BALL_DIMENSION
        )


class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)


# Set up assets
paddle = Paddle()
ball = Ball()
blocks = []
for x in range(
    int(0 + WIDTH / 10), int(WIDTH - WIDTH / 10), BLOCK_WIDTH + BALL_DIMENSION
):
    for y in range(int(0 + HEIGHT / 10), HEIGHT // 2, BLOCK_HEIGHT + BALL_DIMENSION):
        blocks.append(Block(x, y))

# Add start variable
start = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move paddle
    paddle.move(PADDLE_SPEED)
    if (
        pygame.key.get_pressed()[pygame.K_LEFT]
        or pygame.key.get_pressed()[pygame.K_RIGHT]
    ):
        start = True

    # Move ball
    if start:
        ball.move()

    # Collide with walls
    if ball.rect.left < 0 or ball.rect.right > WIDTH:
        ball.speed_x = -ball.speed_x
    if ball.rect.top < 0:
        ball.speed_y = -ball.speed_y

    # Collide with paddle
    if ball.rect.colliderect(paddle.rect):
        ball.speed_y = -ball.speed_y

    # Collide with blocks
    for block in blocks:
        if ball.rect.colliderect(block.rect):
            ball.speed_y = -ball.speed_y
            blocks.remove(block)
            break

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), paddle.rect)
    pygame.draw.rect(screen, (255, 255, 255), ball.rect)
    for block in blocks:
        pygame.draw.rect(screen, (255, 255, 255), block.rect)

    # Flip the display
    pygame.display.flip()

    # End game if ball hits bottom
    if ball.rect.bottom > HEIGHT:
        print("Game Over")
        break
