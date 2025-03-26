import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
SPEED = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Create game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling game speed
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.body = [[WIDTH/2, HEIGHT/2]]
        self.direction = "RIGHT"
        self.new_direction = "RIGHT"
        self.length = 1
        self.score = 0
        self.speed = SPEED

    def move(self):
        # Update direction
        self.direction = self.new_direction
        
        # Move head
        head = self.body[0].copy()
        if self.direction == "RIGHT":
            head[0] += BLOCK_SIZE
        elif self.direction == "LEFT":
            head[0] -= BLOCK_SIZE
        elif self.direction == "UP":
            head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN":
            head[1] += BLOCK_SIZE
            
        # Insert new head
        self.body.insert(0, head)
        
        # Remove tail if not growing
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1
        self.score += 1
        # Increase speed every 3 points
        if self.score % 3 == 0:
            self.speed += 1

class Food:
    def __init__(self):
        self.spawn()
        
    def spawn(self):
        self.position = [
            random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
            random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE
        ]

def check_collision(snake):
    # Wall collision
    if (snake.body[0][0] >= WIDTH or snake.body[0][0] < 0 or
        snake.body[0][1] >= HEIGHT or snake.body[0][1] < 0):
        return True
    
    # Self collision
    for segment in snake.body[1:]:
        if snake.body[0] == segment:
            return True
    return False

def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("comicsansms", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, text_rect)

def game_loop():
    snake = Snake()
    food = Food()
    game_over = False

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.spawn()
                        game_over = False
                else:
                    if event.key in [pygame.K_RIGHT, pygame.K_d] and snake.direction != "LEFT":
                        snake.new_direction = "RIGHT"
                    elif event.key in [pygame.K_LEFT, pygame.K_a] and snake.direction != "RIGHT":
                        snake.new_direction = "LEFT"
                    elif event.key in [pygame.K_UP, pygame.K_w] and snake.direction != "DOWN":
                        snake.new_direction = "UP"
                    elif event.key in [pygame.K_DOWN, pygame.K_s] and snake.direction != "UP":
                        snake.new_direction = "DOWN"

        if not game_over:
            # Game logic
            snake.move()
            
            # Food collision
            if snake.body[0] == food.position:
                snake.grow()
                food.spawn()
                
            # Check for collision
            game_over = check_collision(snake)

        # Drawing
        win.fill(BLACK)
        
        # Draw snake
        for idx, segment in enumerate(snake.body):
            color = GREEN if idx == 0 else BLUE
            pygame.draw.rect(win, color, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw food
        pygame.draw.rect(win, RED, pygame.Rect(food.position[0], food.position[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw score
        draw_text(f"Score: {snake.score}", 35, WHITE, WIDTH//2, 20)
        
        if game_over:
            draw_text("GAME OVER! Press SPACE to restart", 50, RED, WIDTH//2, HEIGHT//2)
            draw_text(f"Final Score: {snake.score}", 40, WHITE, WIDTH//2, HEIGHT//2 + 50)

        pygame.display.update()
        clock.tick(snake.speed)

if __name__ == "__main__":
    game_loop()