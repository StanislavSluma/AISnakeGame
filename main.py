import pygame

pygame.init()

width = 992
height = 496
screen = pygame.display.set_mode((width, height))

running = True


def bg():
    background = pygame.image.load('resources/snakeBg.png').convert_alpha()
    screen.blit(background, (0, 0))


if __name__ == '__main__':
    bg()
    pygame.display.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
