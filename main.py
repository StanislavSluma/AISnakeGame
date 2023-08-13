import pygame

pygame.init()

width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
running = True

if __name__ == '__main__':
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()