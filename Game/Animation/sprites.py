import pygame as pyg
from Utils import helpers
from SheetMusic import import_xml
import time

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


class Notes():
    noir_duration = 60 / import_xml.noir_bpm
    def __init__(self, notes_container):
        self.note_list = import_xml.xml_to_list("Game/SheetMusic/TestSheets/Fly Me To The Moon.xml")
        # print(len(self.note_list))
        # for i, note in enumerate(self.note_list):
        #     if note["duration"] == 0:
        #         print("*********0 Duration note***********")
        #         print(self.note_list[i - 1])
        #         print(note)
        #         print(self.note_list[i + 1])

        self.nb_measures_in_surface = 4
        self.note_index = 0

        self.notes = pyg.sprite.RenderPlain()

        self.notes_container = notes_container

        self.draw_next_note()

        self.last_note_start_time = 0
        self.next_note_duration = self.note_list[0]["duration"] * Notes.noir_duration
    
    
    def draw_next_note(self):
        if self.note_index > len(self.note_list):
            return
        if self.note_list[self.note_index]["note"] == "rest":
            if self.note_index != len(self.note_list) - 1:
                self.next_note_duration = self.note_list[self.note_index + 1]["duration"] * Notes.noir_duration
            self.note_index += 1
        else:
            self.notes.add(Note(self.notes_container,self.note_list[self.note_index]))
            if self.note_index != len(self.note_list) - 1:
                self.next_note_duration = self.note_list[self.note_index + 1]["duration"] * Notes.noir_duration
            self.note_index += 1
            self.last_note_start_time = time.time()


    def update(self):
        if time.time() - self.last_note_start_time > self.next_note_duration:
            self.draw_next_note()
        self.notes.update()


    def kill_notes(self):
        for note in self.notes:
            if note.rect.x > self.width:
                note.kill()


class Note(pyg.sprite.Sprite):
    def __init__(self, parent_surface, note):
        pyg.sprite.Sprite.__init__(self)
        color = (200, 200, 200)
        radius = 5
        noir_base_width = 120
        duration = 0.25 if note["duration"] == 0 else note["duration"]
        width = duration * noir_base_width
        self.velocity = (width / (duration * Notes.noir_duration)) / 30
        y_padding = 4
        self.parent_container_height = parent_surface.get_rect().height
        height = (self.parent_container_height / helpers.total_nb_notes)
        
        x_start_pos = noir_base_width * -4
        y_pos = self.parent_container_height - helpers.note_dict[note["note"]] * height

        self.image = pyg.Surface([width, height])
        self.image.fill(color)
        self.image.set_colorkey(color)
        pyg.draw.rect(self.image, (255, 255, 255), [0, 0, width, height - y_padding])
        
        self.rect = self.image.get_rect()

        label = helpers.text(note["note"], helpers.colors["text1"], helpers.colors["background1"], 20)
        self.image.blit(label, (10, 10))

        self.rect.x = x_start_pos
        self.rect.y = y_pos

    
    def update(self):
        self.rect.move_ip([self.velocity, 0])