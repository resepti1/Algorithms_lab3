import pygame
import os
from scipy.spatial import ConvexHull

x = []
y = []

# отримання директорії скріпта
script_directory = os.path.dirname(os.path.abspath(__file__))

# отримання шляху зберігання результату
output_image_path = os.path.join(script_directory, "output.jpg")

# зчитування координат з файлу
with open('DS7.txt', 'r') as file:
    for line in file:
        coordinates = line.split()
        y.append(int(coordinates[0]))
        x.append(int(coordinates[1]))

points = list(zip(x, y))

# створення об'єкту ConvexHull тобто опуклої оболонки
hull = ConvexHull(points)

# знаходження координат точок опуклої оболонки
hull_indices = hull.vertices
convex_hull_x = [x[i] for i in hull_indices]
convex_hull_y = [y[i] for i in hull_indices]

# ініціалізація pygame і її параметрів
pygame.init()

width, height = 960, 540
point_color = (0, 0, 0) 

center_x = width // 2
center_y = height // 2

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lab2")


font = pygame.font.Font(None, 36)

text_X = font.render("X", True, (255,0,0))
text_Y = font.render("Y", True, (255,0,0))

running = True

#цикл вікна
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # очищення екрану
    screen.fill((255, 255, 255))  # Заполнение экрана черным цветом

        # виведення точок опуклої оболонки
    for i in range(len(convex_hull_x)):
        convex_hull_reflected_y = height - convex_hull_y[i]
        pygame.draw.circle(screen, 'blue', (convex_hull_x[i], convex_hull_reflected_y), 4)

        # виведення всього датасету
    for i in range(len(x)):
        reflected_y = height - y[i]
        pygame.draw.circle(screen, point_color, (x[i], reflected_y), 1)

        # з'єднання точок опуклої оболонки червоними відрізками
    for i in range(len(convex_hull_x)):
        if i!=0:
            previous_x = convex_hull_x[i-1]
            previous_y = height - convex_hull_y[i-1]
            current_x = convex_hull_x[i]
            current_y = height - convex_hull_y[i]
            pygame.draw.line(screen, 'red', (previous_x, previous_y), (current_x, current_y))
        else:
            last_x = convex_hull_x[-1]
            last_y = height - convex_hull_y[-1]
            first_x = convex_hull_x[0]
            first_y = height - convex_hull_y[0]
            pygame.draw.line(screen, 'red', (last_x, last_y), (first_x, first_y))

    
    # виведення осі Х
    pygame.draw.line(screen, (0, 0, 0), (4, height), (4, 0), 2)

    # виведення осі У
    pygame.draw.line(screen, (0, 0, 0), (4, height - 4), (width, height-4), 2)
    
    # виведення тексту
    screen.blit(text_Y, (10,1))
    screen.blit(text_X, (width - 20, height - 30))

    # Оновелння екрану
    pygame.display.flip()

# збереження результату
pygame.image.save(screen, output_image_path)
convex_hull_output_path = os.path.join(script_directory, "convex_hull_points.txt")

# збереження датасету опуклої оболнки в окремий файл
with open(convex_hull_output_path, 'w') as output_file:
    for i in hull_indices:
        output_file.write(f"{x[i]} {y[i]}\n")

# Завершення Pygame
pygame.quit()
