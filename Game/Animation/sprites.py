import pygame as pyg
import math

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

    def update(self, pitch, upper_pitch, lower_pitch):
        if pitch == 0:
            pass
        else:
            self.target_y = math.floor((self.parent_container_height - self.rect.width) * (1 - ((pitch - lower_pitch) / (upper_pitch - lower_pitch))))
        if self.rect.y < self.target_y - self.velocity_y or self.rect.y > self.target_y + self.velocity_y:
            if self.rect.y > self.target_y:
                self.rect.move_ip([0, (abs(self.rect.y - self.target_y) / 2) * -1])
            else:
                self.rect.move_ip([0, (abs(self.rect.y - self.target_y) / 2)])