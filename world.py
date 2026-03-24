import numpy as np
import random

# Константы мира
GRID_SIZE = (50, 50)  # Размер мира
CELL_SIZE = 10  # Размер клетки в пикселях

# Определение типов клеток
EMPTY = 0
GRASS = 1
WATER = 2
FOREST = 3
DESERT = 4

# Инициализация мира
def generate_world():
    world = np.zeros(GRID_SIZE, dtype=int)

    # Заполняем клетками
    for x in range(GRID_SIZE[0]):
        for y in range(GRID_SIZE[1]):
            choice = random.random()
            if choice < 0.6:
                world[x, y] = GRASS  # Трава - 60%
            elif choice < 0.75:
                world[x, y] = WATER  # Вода - 15%
            elif choice < 0.9:
                world[x, y] = FOREST  # Лес - 15%
            else:
                world[x, y] = DESERT  # Пустыня - 10%

    return world
