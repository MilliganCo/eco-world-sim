import pygame
from world import generate_world
from creatures import generate_creatures, update_creatures
from events import log_event, generate_event, render_terminal

# Константы
GRID_SIZE = (50, 50)
CELL_SIZE = 10
SCREEN_SIZE = (GRID_SIZE[0] * CELL_SIZE, GRID_SIZE[1] * CELL_SIZE + 150)

# Цвета существ
CREATURE_COLORS = {
    5: (255, 255, 0),  # 🦌 Травоядные (жёлтые)
    6: (255, 0, 0),    # 🐺 Хищники (красные)
}

# Инициализация
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Генерация мира и существ
world = generate_world()
creatures = generate_creatures(GRID_SIZE)

turn_counter = 0
running = True
show_menu = False  # Флаг показа справки

# Функция отрисовки меню
def render_menu(screen, font):
    """Рисует справочное меню."""
    pygame.draw.rect(screen, (40, 40, 40), (50, 50, 400, 300))  # Затемненный фон меню
    text = font.render("СПРАВОЧНОЕ МЕНЮ", True, (255, 255, 255))
    screen.blit(text, (60, 60))

    descriptions = [
        "🌿 Трава - еда для травоядных",
        "💧 Вода - источник жизни",
        "🌲 Лес - убежище и источник пищи",
        "🏜 Пустыня - суровая местность",
        "🦌 Травоядные - питаются травой",
        "🐺 Хищники - охотятся на травоядных"
    ]

    y_offset = 100
    for desc in descriptions:
        text = font.render(desc, True, (200, 200, 200))
        screen.blit(text, (60, y_offset))
        y_offset += 30

    text = font.render("Нажмите TAB для закрытия", True, (255, 200, 100))
    screen.blit(text, (60, 310))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                show_menu = not show_menu  # Переключаем флаг справки

    if not show_menu:
        turn_counter += 1
        creatures = update_creatures(world, creatures)

        # Генерация событий раз в 5 ходов
        if turn_counter % 5 == 0:
            generate_event(turn_counter, world, creatures)

        # Отрисовка мира
        screen.fill((0, 0, 0))  # Черный фон вместо зелёного
        for x in range(GRID_SIZE[0]):
            for y in range(GRID_SIZE[1]):
                color = (50, 50, 50)  # По умолчанию пустая клетка
                if world[x, y] == 1:
                    color = (0, 200, 0)  # Трава
                elif world[x, y] == 2:
                    color = (0, 0, 255)  # Вода
                elif world[x, y] == 3:
                    color = (0, 100, 0)  # Лес
                elif world[x, y] == 4:
                    color = (200, 200, 50)  # Пустыня

                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Отрисовка существ
        for x in range(GRID_SIZE[0]):
            for y in range(GRID_SIZE[1]):
                if creatures[x, y] in CREATURE_COLORS:
                    pygame.draw.circle(
                        screen,
                        CREATURE_COLORS[creatures[x, y]],
                        (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3
                    )

        # Отрисовка терминала
        render_terminal(screen, font, SCREEN_SIZE, GRID_SIZE)

    else:
        render_menu(screen, font)  # Отображаем справку поверх игры

    pygame.display.flip()
    clock.tick(2)
