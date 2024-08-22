import pygame
import random

# Initialize pygame
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Function to generate a random starting position for the snake and target
def generate_starting_position():
    position_range = (pixel_width // 2, screen_width - pixel_width // 2, pixel_width)
    return [random.randrange(*position_range), random.randrange(*position_range)]

# Function to move the snake
def move_snake():
    global snake_direction
    new_head = snake[0].move(snake_direction)
    snake.insert(0, new_head)
    snake.pop()

# Function to check for collisions with walls or itself
def check_collision():
    head = snake[0]
    if head.left < 0 or head.right > screen_width or head.top < 0 or head.bottom > screen_height:
        return True
    for segment in snake[1:]:
        if head.colliderect(segment):
            return True
    return False

# Function to check if the snake has collided with the target
def check_food_collision():
    return snake[0].colliderect(target)

# Function to place the target at a new position
def place_target():
    while True:
        target.center = generate_starting_position()
        if not any(target.colliderect(segment) for segment in snake):
            break

# Function to get the new direction based on user input
def get_new_direction():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and snake_direction != (0, pixel_width):
        return (0, -pixel_width)
    if keys[pygame.K_s] and snake_direction != (0, -pixel_width):
        return (0, pixel_width)
    if keys[pygame.K_a] and snake_direction != (pixel_width, 0):
        return (-pixel_width, 0)
    if keys[pygame.K_d] and snake_direction != (-pixel_width, 0):
        return (pixel_width, 0)
    return snake_direction

# Width of the snake
pixel_width = 50

# Initialize the snake
snake_pixel = pygame.Rect([0, 0, pixel_width, pixel_width])
snake_pixel.center = generate_starting_position()
snake = [snake_pixel.copy()]

snake_direction = (0, 0)

# Initialize the target
target = pygame.Rect([0, 0, pixel_width, pixel_width])
place_target()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    snake_direction = get_new_direction()

    move_snake()

    if check_collision():
        running = False

    if check_food_collision():
        place_target()
        snake.append(snake[-1].copy())

    screen.fill("black")

    for snake_part in snake:
        pygame.draw.rect(screen, "green", snake_part)

    pygame.draw.rect(screen, "red", target)

    pygame.display.flip()

    clock.tick(15)

pygame.quit()
