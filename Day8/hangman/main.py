"""import pygame

# Initialiser pygame
pygame.init()

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# Boucle principale
running = True
while running:
    # Parcourir les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualiser l’écran
    pygame.display.flip()

# Quitter pygame
pygame.quit()"""

import pygame
import os

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# Charger fond
background_img = pygame.image.load(os.path.join("assets", "background.png"))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


def draw_stickman(surface, x, y):
    head_radius = 20
    body_length = 60
    arm_length = 40
    leg_length = 50
    color = (0, 0, 0)

    # Tête
    pygame.draw.circle(surface, color, (x, y + head_radius), head_radius, 2)
    # Corps
    start_body = (x, y + 2 * head_radius)
    end_body = (x, y + 2 * head_radius + body_length)
    pygame.draw.line(surface, color, start_body, end_body, 2)

    # Bras
    pygame.draw.line(surface, color, (x, y + 2 * head_radius + 10), (x - arm_length, y + 2 * head_radius + 10), 2)
    pygame.draw.line(surface, color, (x, y + 2 * head_radius + 10), (x + arm_length, y + 2 * head_radius + 10), 2)

    # Jambes
    pygame.draw.line(surface, color, end_body, (x - leg_length, y + 2 * head_radius + body_length + leg_length), 2)
    pygame.draw.line(surface, color, end_body, (x + leg_length, y + 2 * head_radius + body_length + leg_length), 2)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Affichage
    screen.blit(background_img, (0, 0))
    draw_stickman(screen, WIDTH // 2, 100)

    pygame.display.flip()
pygame.quit()

