import pygame as pyg
from Utils import helpers

class PitchIndicator(pyg.sprite.Sprite):
    def __init__(self, parent_surface):
        pyg.sprite.Sprite.__init__(self)
        self.image = pyg.image.load('Game/Animation/assets/images/pick.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.parent_container_height = parent_surface.get_rect().height
        self.rect.y = (self.parent_container_height / 2) - (self.rect.width / 2)

        self.target_y = self.rect.y

        self.velocity_y = 6

        self.note_height = (self.parent_container_height / helpers.total_nb_notes)

    def update(self, note):
        if note == "none":
            pass
        else:
            self.target_y = self.parent_container_height - (helpers.note_dict[note] * self.note_height) + (self.note_height / 2)
        if self.rect.y < self.target_y - self.velocity_y or self.rect.y > self.target_y + self.velocity_y:
            if self.rect.y > self.target_y:
                self.rect.move_ip([0, (abs(self.rect.y - self.target_y) / 2) * -1])
            else:
                self.rect.move_ip([0, (abs(self.rect.y - self.target_y) / 2)])


class Note(pyg.sprite.Sprite):
    def __init__(self, parent_surface, note):
        pyg.sprite.Sprite.__init__(self)
        color = (200, 200, 200)
        radius = 5
        base_width = 100
        width = note["duration"] * base_width
        y_padding = 4
        self.parent_container_height = parent_surface.get_rect().height
        height = (self.parent_container_height / helpers.total_nb_notes)
        
        x_start_pos = parent_surface.get_rect().width - width # should be note["start"]
        y_pos = self.parent_container_height - helpers.note_dict[note["note"]] * height

        self.image = pyg.Surface([width, height])
        self.image.fill(color)
        self.image.set_colorkey(color)
        pyg.draw.rect(self.image, (255, 255, 255), [0, 0, width, height - y_padding], radius)
        
        self.rect = self.image.get_rect()

        label = helpers.text(note["note"], helpers.colors["text1"], helpers.colors["background1"], 14)
        self.image.blit(label, (10, 10))

        self.rect.x = x_start_pos
        self.rect.y = y_pos

    
    def update(self):
        pass