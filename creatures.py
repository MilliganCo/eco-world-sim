import numpy as np
import random

# Определение существ
HERBIVORE = 5  # Травоядные
PREDATOR = 6  # Хищники

# Добавляем счётчик голода хищникам и эффект ускорения
hunger = {}
predator_boost = {}  # Когда хищник ускоряется
boost_cooldown = {}  # Кулдаун между ускорениями

def generate_creatures(grid_size, num_herbivores=60, num_predators=15):
    """Генерирует начальное распределение существ."""
    creatures = np.zeros(grid_size, dtype=int)

    for _ in range(num_herbivores):
        x, y = random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1)
        creatures[x, y] = HERBIVORE

    for _ in range(num_predators):
        x, y = random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1)
        creatures[x, y] = PREDATOR
        hunger[(x, y)] = 5  # Хищники теперь живут дольше без еды
        boost_cooldown[(x, y)] = 0  # Таймер для ускорения

    return creatures

def find_nearest_food(world, x, y):
    """Ищет ближайшую траву в радиусе 3 клеток"""
    for radius in range(1, 4):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = (x + dx) % world.shape[0], (y + dy) % world.shape[1]
                if world[nx, ny] == 1:  # Если найдена трава
                    return nx, ny
    return None

def find_nearest_prey(creatures, x, y):
    """Ищет ближайшее травоядное в радиусе 2 клеток"""
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            nx, ny = (x + dx) % creatures.shape[0], (y + dy) % creatures.shape[1]
            if creatures[nx, ny] == HERBIVORE:
                return nx, ny
    return None

def count_neighbors(creatures, x, y, creature_type):
    """Считает, сколько существ определённого типа рядом"""
    count = 0
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % creatures.shape[0], (y + dy) % creatures.shape[1]
            if creatures[nx, ny] == creature_type:
                count += 1
    return count

def update_creatures(world, creatures):
    """Обновляет позиции существ и их взаимодействие."""
    global hunger, predator_boost, boost_cooldown
    new_creatures = np.zeros_like(creatures)
    new_hunger = {}

    for x in range(world.shape[0]):
        for y in range(world.shape[1]):
            if creatures[x, y] == HERBIVORE:
                food = find_nearest_food(world, x, y)

                if food:
                    nx, ny = food  # Травоядное движется к траве
                    world[nx, ny] = 0  # Травоядное съедает траву
                else:
                    dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                    nx, ny = (x + dx) % world.shape[0], (y + dy) % world.shape[1]

                # Травоядные избегают пустыни, если могут
                if world[nx, ny] == 4 and random.random() < 0.8:
                    nx, ny = x, y  # Остаются на месте

                new_creatures[nx, ny] = HERBIVORE

                # Бонус размножения, если рядом есть другие травоядные
                neighbor_bonus = count_neighbors(creatures, x, y, HERBIVORE) * 0.005
                reproduction_chance = 0.03 + neighbor_bonus

                # Травоядные размножаются быстрее в траве, но медленнее в пустыне
                if world[x, y] == 1:
                    reproduction_chance += 0.01
                elif world[x, y] == 4:
                    reproduction_chance -= 0.01

                if random.random() < reproduction_chance:
                    new_creatures[x, y] = HERBIVORE

                # Трава растёт обратно через 5 ходов
                if world[x, y] == 0 and random.random() < 0.02:
                    world[x, y] = 1

            elif creatures[x, y] == PREDATOR:
                prey = find_nearest_prey(creatures, x, y)

                # Если вокруг 3+ травоядных, хищник ускоряется на 2 хода (раз в 10 ходов)
                if count_neighbors(creatures, x, y, HERBIVORE) >= 3 and boost_cooldown.get((x, y), 0) <= 0:
                    predator_boost[(x, y)] = 2
                    boost_cooldown[(x, y)] = 10

                if predator_boost.get((x, y), 0) > 0:
                    predator_boost[(x, y)] -= 1  # Ускоренный режим
                    dx, dy = random.choice([(0, 2), (2, 0), (0, -2), (-2, 0)])
                else:
                    dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])

                nx, ny = (x + dx) % world.shape[0], (y + dy) % world.shape[1]

                # Если есть цель – идём к ней
                if prey:
                    nx, ny = prey  # Хищник двигается к ближайшему травоядному

                # Травоядные могут прятаться в лесу (хищник не видит их)
                if world[nx, ny] == 3 and random.random() < 0.8:
                    new_creatures[x, y] = PREDATOR  # Хищник "теряет" травоядное

                elif creatures[nx, ny] == HERBIVORE:
                    if random.random() > 0.5:  # 50% шанс побега
                        new_creatures[nx, ny] = PREDATOR
                        new_hunger[(nx, ny)] = 5  # Хищник поел
                    else:
                        new_creatures[x, y] = PREDATOR  # Травоядное убежало

                else:
                    new_creatures[nx, ny] = PREDATOR
                    new_hunger[(nx, ny)] = hunger.get((x, y), 5) - 1

                # Кулдаун на ускорение
                if boost_cooldown.get((x, y), 0) > 0:
                    boost_cooldown[(x, y)] -= 1

                # Хищник умирает, если не ел 5 ходов
                if new_hunger.get((nx, ny), 0) <= 0:
                    new_creatures[nx, ny] = 0

    return new_creatures
