import pygame
import os
pygame.init()
win = pygame.display.set_mode((1024, 600))
background_image = pygame.transform.scale(pygame.image.load("images/Map.png"), (1024, 600))
clock = pygame.time.Clock()
points = []
# coordinate of the rect surface
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        win.blit(background_image, (0, 0))
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            points.append((x, y))

    # draw window
    #win.fill((0, 0, 0))
    # draw point
    for p in points:
        pygame.draw.circle(win, (255, 0, 0), p, 5)
    pygame.display.update()
pygame.quit()

with open('path_point.txt', 'w') as f:
    f.write(f"{points}")
