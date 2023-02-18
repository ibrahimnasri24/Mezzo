from Utils import helpers
from SheetMusic import import_xml
import pygame as pyg

class Button:
    def __init__(self, parent_surface, file, x, y, width, height, menu_top_padding, menu_left_padding):
        self.label = file["name"]
        self.x = x
        self.y = y
        self.y_rel_to_screen = y + menu_top_padding
        self.x_rel_to_screen = x + menu_left_padding
        self.width = width
        self.padding = 10
        self.height = height
        self.parent_surface = parent_surface
        self.button_surface = pyg.Surface((self.width,self.height), pyg.SRCALPHA, 32)

    def draw_button(self, mouse_x, mouse_y):
        if mouse_x > self.x and mouse_x < self.x + self.width and mouse_y > self.y_rel_to_screen and mouse_y < self.y_rel_to_screen + self.height:
            self.button_surface.fill((90,90,90))
        else:
            self.button_surface.fill((40,40,40))

        label_text = helpers.text(self.label, (150,150,150), helpers.colors["background1"], 28)
        self.button_surface.blit(label_text, (self.padding, self.padding))
        
        self.parent_surface.blit(self.button_surface, (self.x, self.y))

class Menu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.menu_top_padding = 50
        self.menu_left_padding = 50
        self.width = 1280
        self.height = 700
        self.menu_container = pyg.Surface((self.width,self.height), pyg.SRCALPHA, 32)
        self.files = import_xml.get_files_from_sheets_directory()
        
        self.buttons = []
        button_width = self.width
        button_height = 60

        for i, file in enumerate(self.files):
            self.buttons.append(Button(self.menu_container, file, 0, i * button_height + 100, button_width, button_height, self.menu_top_padding, self.menu_left_padding))


    def draw_file_picker(self):
        pass


    def draw_main_menu(self, mouse_x, mouse_y):
        scale  = 0.8
        GB = min(255, max(0, round(255 * (1-scale))))
        self.screen.fill((0, GB, GB), special_flags = pyg.BLEND_MULT)

        menu = helpers.text('Menu', (200,200,200), helpers.colors["background1"], 50)
        self.menu_container.blit(menu, (0, 0))

        for button in self.buttons:
            button.draw_button(mouse_x, mouse_y)

        self.screen.blit(self.menu_container, (self.menu_left_padding , self.menu_top_padding))

    def click_handler(self, mouse_coordinates):
        for button in self.buttons:
            if mouse_coordinates[0] > button.x_rel_to_screen and mouse_coordinates[0] < button.x_rel_to_screen + button.width and mouse_coordinates[1] > button.y_rel_to_screen and mouse_coordinates[1] < button.y_rel_to_screen + button.height:
                print(button.label)
            