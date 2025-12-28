"""Простая игра Змейка на pygame."""

import random
import sys

import pygame

# Константы
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 8

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def get_random_food_position(snake):
    """Возвращает случайную позицию еды, не пересекающуюся со змейкой."""
    while True:
        position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        if position not in snake:
            return position


def main():
    """Главная функция игры."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = RIGHT
    food = get_random_food_position(snake)
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

        # Движение
        head_x = (snake[0][0] + direction[0]) % GRID_WIDTH
        head_y = (snake[0][1] + direction[1]) % GRID_HEIGHT
        new_head = (head_x, head_y)

        # Проверка на столкновение с собой
        if new_head in snake:
            running = False
        else:
            snake.insert(0, new_head)
            if new_head == food:
                score += 1
                food = get_random_food_position(snake)
            else:
                snake.pop()

        # Отрисовка
        screen.fill(BLACK)

        # Змейка
        for segment in snake:
            pygame.draw.rect(
                screen, GREEN, (*[c * GRID_SIZE for c in segment], GRID_SIZE, GRID_SIZE)
            )

        # Еда
        pygame.draw.rect(
            screen, RED, (*[c * GRID_SIZE for c in food], GRID_SIZE, GRID_SIZE)
        )

        # Счёт
        text = font.render(f"Счёт: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
