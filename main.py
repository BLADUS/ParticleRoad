import pygame
import random
import math
import sys
import matplotlib.pyplot as plt

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Инициализация Pygame
pygame.init()

# Настройка окна
window_size = (400, 400)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Движение частиц")

# Параметры окружности
center = (200, 200)
radius = 150
circle_color = WHITE

# Параметры частиц
particle_radius = 10

# Переменные для движения частиц
step_count = 0
num_particles = 1  # Начальное количество частиц
angles = [0] * num_particles  # Начальные углы для движения частиц
particle_colors = [pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in
                   range(num_particles)]  # Генерация случайных цветов для частиц

intensity_values = []  # Список для хранения значений интенсивности
average_moves_values = []  # Список для хранения средних перемещений
average_speed_values = []  # Список для хранения средних скоростей

clock = pygame.time.Clock()


def calculate_average_moves():
    total_moves = 0
    num_trials = 10  # Количество прогонов для расчета среднего количества перемещений

    for _ in range(num_trials):
        angles = [0] * num_particles
        moves = 0
        while True:
            for i in range(num_particles):
                if random.random() < 0.6:  # 60% шанс перемещения на следующую позицию
                    angles[i] += 0.05
            moves += 1
            if all(angle >= 2 * math.pi for angle in angles):
                break
        total_moves += moves
    return total_moves / num_trials


def calculate_intensity():
    angles = [0] * num_particles
    intensity = 0

    while True:
        for i in range(num_particles):
            if random.random() < 0.6:  # 60% шанс перемещения на следующую позицию
                angles[i] += 0.05
        intensity += 1
        if all(angle >= 2 * math.pi for angle in angles):
            break

    return intensity


def calculate_average_speed():
    total_speed = 0
    num_trials = 10  # Количество прогонов для расчета средней скорости

    for _ in range(num_trials):
        angles = [0] * num_particles
        moves = 0
        while True:
            for i in range(num_particles):
                if random.random() < 0.6:  # 60% шанс перемещения на следующую позицию
                    angles[i] += 0.05
            moves += 1
            if all(angle >= 2 * math.pi for angle in angles):
                break
        speed = moves / (2 * math.pi)
        total_speed += speed
    return total_speed / num_trials


def update_particles(num):
    global num_particles, angles, particle_colors, intensity_values, average_moves_values, average_speed_values

    num_particles = num
    angles = [0] * num_particles
    particle_colors = [pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in
                       range(num_particles)]


def draw_text(surface, text, pos):
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, WHITE)
    surface.blit(text_surface, pos)


done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                num_particles += 1
                update_particles(num_particles)
            elif event.key == pygame.K_DOWN:
                if num_particles > 1:
                    num_particles -= 1
                    update_particles(num_particles)

    screen.fill(BLACK)

    # Отрисовка окружности
    pygame.draw.circle(screen, circle_color, center, radius, 2)

    # Отрисовка частиц
    for i in range(num_particles):
        particle_x = center[0] + int(radius * math.cos(angles[i]))
        particle_y = center[1] + int(radius * math.sin(angles[i]))
        pygame.draw.circle(screen, particle_colors[i], (particle_x, particle_y), particle_radius)

        # Проверка достижения конца окружности
        if angles[i] >= 2 * math.pi:
            angles[i] = 0
            particle_colors[i] = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            num_particles -= 1

        # Отрисовка счетчика выполненных шагов и среднего количества перемещений
    draw_text(screen, "Шаги: " + str(step_count), (10, 10))
    draw_text(screen, "Среднее перемещений: " + str(calculate_average_moves()), (10, 40))
    draw_text(screen, "Средняя скорость: " + str(calculate_average_speed()), (10, 70))
    draw_text(screen, "Количество частиц: " + str(num_particles), (10, 100))

    pygame.display.flip()

    for i in range(num_particles):
        if random.random() < 0.6:
            angles[i] += 0.05  # Изменение углов движения

    step_count += 1

    if num_particles == 0:
        done = True

    intensity_values.append(calculate_intensity())
    average_moves_values.append(calculate_average_moves())
    average_speed_values.append(calculate_average_speed())

    clock.tick(60)

print("Частицы завершили полный оборот!")
print("Общее количество шагов:", step_count)

# Отображение графика интенсивности
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.plot(range(len(intensity_values)), intensity_values)
plt.xlabel('Шаги')
plt.ylabel('Интенсивность')
plt.title('График интенсивности')

# Отображение графика средних перемещений
plt.subplot(1, 2, 2)
plt.plot(range(len(average_moves_values)), average_moves_values)
plt.xlabel('Шаги')
plt.ylabel('Средние перемещения')
plt.title('График средних перемещений')

plt.tight_layout()
plt.show()

# Отображение графика средней скорости
plt.figure()
plt.plot(range(len(average_speed_values)), average_speed_values)
plt.xlabel('Шаги')
plt.ylabel('Средняя скорость')
plt.title('График средней скорости')
plt.show()

pygame.quit()
sys.exit()