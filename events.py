import pygame
import numpy as np

TERMINAL_HEIGHT = 150
log_messages = []
previous_stats = {"herbivores": 0, "predators": 0}  # Предыдущие популяции


def log_event(message, color=(255, 255, 255)):
    """Добавляет событие в лог с цветом."""
    if len(log_messages) > 5:
        log_messages.pop(0)
    log_messages.append((message, color))


def generate_event(turn_counter, world, creatures):
    """Генерация событий, влияющих на мир."""
    global previous_stats

    herbivores = np.sum(creatures == 5)
    predators = np.sum(creatures == 6)

    # Проверка роста популяции
    if turn_counter % 10 == 0:
        herb_growth = ((herbivores - previous_stats["herbivores"]) / (previous_stats["herbivores"] + 1)) * 100
        pred_growth = ((predators - previous_stats["predators"]) / (previous_stats["predators"] + 1)) * 100

        if herb_growth > 20:
            log_event(f"🦌 Травоядные увеличились на {int(herb_growth)}%!", (0, 200, 0))
        elif herb_growth < -20:
            log_event(f"⚠ Травоядные уменьшились на {int(abs(herb_growth))}%!", (255, 100, 100))

        if pred_growth > 20:
            log_event(f"🐺 Хищники увеличились на {int(pred_growth)}%!", (200, 0, 0))
        elif pred_growth < -20:
            log_event(f"⚠ Хищники уменьшились на {int(abs(pred_growth))}%!", (255, 50, 50))

        previous_stats["herbivores"] = herbivores
        previous_stats["predators"] = predators

    # События мира
    if turn_counter % 10 == 0:
        log_event(f"🌱 Лес разрастается!", (50, 200, 50))
        for _ in range(20):
            x, y = np.random.randint(0, world.shape[0]), np.random.randint(0, world.shape[1])
            if world[x, y] == 1:
                world[x, y] = 3

    if turn_counter % 15 == 0:
        log_event(f"🔥 Лес загорелся! Огонь распространяется.", (255, 150, 50))
        for _ in range(10):
            x, y = np.random.randint(0, world.shape[0]), np.random.randint(0, world.shape[1])
            if world[x, y] == 3:
                world[x, y] = 1

    if turn_counter % 20 == 0:
        log_event(f"💧 Засуха! Вода испаряется.", (0, 150, 255))
        for _ in range(10):
            x, y = np.random.randint(0, world.shape[0]), np.random.randint(0, world.shape[1])
            if world[x, y] == 2:
                world[x, y] = 4


def render_terminal(screen, font, screen_size, grid_size):
    """Рисует терминал внизу экрана."""
    pygame.draw.rect(screen, (30, 30, 30), (0, grid_size[1] * 10, screen_size[0], TERMINAL_HEIGHT))

    for i, (msg, color) in enumerate(log_messages):
        text = font.render(msg, True, color)
        screen.blit(text, (10, grid_size[1] * 10 + 10 + i * 20))
