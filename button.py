import pygame


class Button:
    def __init__(self, pos, text, font, text_color, screen):
        self.__x = pos[0]
        self.__y = pos[1]
        self.__screen = screen
        self.__font = font
        self.__text = text
        self.__text_color = text_color
        self.__rendered_text = self.__font.render(text, True, pygame.Color('white'))
        self.__text_rect = self.__rendered_text.get_rect(center=(self.__x, self.__y))

        self.__width = self.__rendered_text.get_width()
        self.__height = self.__rendered_text.get_height()

        self.__button_rect = pygame.rect.Rect(self.__x, self.__y, self.__width, self.__height)

    def change_color(self, mouse_pos):
        if mouse_pos[0] in range(int(self.__x - self.__width), int(self.__x)) and mouse_pos[1] in range(int(self.__y - self.__height), int(self.__y)):
            self.__rendered_text = self.__font.render(self.__text, True, self.__text_color)
        else:
            self.__rendered_text = self.__font.render(self.__text, True, pygame.Color('white'))

    def update(self):
        self.__screen.blit(self.__rendered_text, self.__text_rect)

    def check_input(self, mouse_pos):
        if mouse_pos[0] in range(int(self.__x - self.__width), int(self.__x)) and mouse_pos[1] in range(int(self.__y - self.__height), int(self.__y)):
            return True
        else:
            return False
