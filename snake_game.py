"""Классическая игра «Змейка» на Pygame."""

import pygame
import random
from typing import List, Tuple

# Константы игры
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

# Направления движения (dx, dy)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


class GameObject:
    """Базовый класс для игровых объектов (змейка и яблоко)."""

    def __init__(self, position: Tuple[int, int] = None, body_color: Tuple[int, int] = None):
        """Инициализирует объект с позицией и цветом."""
        self.position = position or CENTER_POSITION
        self.body_color = body_color

    def draw(self, surface: pygame.Surface) -> None:
        """Абстрактный метод отрисовки. Переопределяется в дочерних классах."""
        pass

    def draw_cell(self, surface: pygame.Surface, position: Tuple[int, int], color: Tuple[int, int]) -> None:
        """Отрисовывает одну ячейку по заданным координатам и цвету."""
        rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, color, rect)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализирует яблоко красного цвета в случайной позиции."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position([])  # изначально змейка пуста

    def randomize_position(self, snake_positions: List[Tuple[int, int]]) -> None:
        """Генерирует случайную позицию, не совпадающую с позициями змейки."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко."""
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions: List[Tuple[int, int]] = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self) -> None:
        """Применяет отложенное изменение направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple: Apple) -> None:
        """Обновляет позицию змейки с учётом направления и столкновений."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        # Проверка самоукуса (невозможно для короткой змейки)
        if len(self.positions) > 3 and new_head in self.positions[2:]:
            self.reset()
            return

        self.last = self.positions[-1] if len(self.positions) >= self.length else None
        self.positions.insert(0, new_head)

        if new_head == apple.position:
            self.length += 1
            apple.randomize_position(self.positions)
        elif len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку и стирает хвост."""
        if self.last:
            self.draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR)

        for position in self.positions:
            self.draw_cell(surface, position, self.body_color)
            # Обводка для красоты
            border_rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (93, 216, 93), border_rect, 1)

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(snake: Snake) -> None:
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main() -> None:
    """Основной игровой цикл."""
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')

    apple = Apple()
    snake = Snake()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()
