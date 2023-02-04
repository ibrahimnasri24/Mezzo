import pygame as pyg
from Utils import helpers
from SheetMusic import import_xml
import time
from Animation import animation
from Animation import logic

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
        self.note_list = import_xml.xml_to_list("Game/SheetMusic/TestSheets/test.xml")
        self.nb_measures_in_surface = 4
        self.note_index = 0

        self.notes = pyg.sprite.RenderPlain()

        self.notes_container = notes_container

        self.draw_next_note()

        self.last_note_start_time = 0
        self.next_note_duration = self.note_list[0]["duration"] * Notes.noir_duration


    def draw_next_note(self):
        if self.note_index > len(self.note_list) - 1:
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


    def update(self, played_note):
        if time.time() - self.last_note_start_time > self.next_note_duration:
            self.draw_next_note()
        self.notes.update(played_note)


    def kill_notes(self):
        for note in self.notes:
            if note.rect.x > self.width:
                note.kill()


class Note(pyg.sprite.Sprite):
    logic = logic.Logic.get_instance()
    print(logic)
    def __init__(self, parent_surface, note):
        pyg.sprite.Sprite.__init__(self)
        color = (200, 200, 200)
        radius = 8
        noir_base_width = 120
        duration = 0.25 if note["duration"] == 0 else note["duration"]
        self.width = duration * noir_base_width
        self.velocity = (self.width / (duration * Notes.noir_duration)) / 30
        y_padding = 4
        self.parent_container_height = parent_surface.get_rect().height
        self.parent_container_width = parent_surface.get_rect().width
        height = (self.parent_container_height / helpers.total_nb_notes)
        
        self.note_with_octave = note["note"]

        x_start_pos = noir_base_width * -4
        y_pos = self.parent_container_height - helpers.note_dict[self.note_with_octave] * height

        self.image = pyg.Surface([self.width, height])
        self.image.fill(color)
        self.image.set_colorkey(color)
        pyg.draw.rect(self.image, (255, 255, 255), [0, 0, self.width, height - y_padding], 0, radius)
        
        self.rect = self.image.get_rect()

        label = helpers.text(self.note_with_octave, helpers.colors["text1"], helpers.colors["background1"], 20)
        self.image.blit(label, (10, 10))

        self.rect.x = x_start_pos
        self.rect.y = y_pos
        self.inside_note = False
        self.finished_note = False

        self.max_hits_per_note = duration * Notes.noir_duration * 30
        self.note_hit = 0
        self.note_hite_rate = 0

    
    def update(self, played_note):
        self.rect.move_ip([self.velocity, 0])

        if self.rect.x + self.width > self.parent_container_width - animation.Animation.indicator_container_width:
            if self.rect.x < self.parent_container_width - animation.Animation.indicator_container_width:
                if not self.inside_note:
                    # print("inside note {}".format(self.note_with_octave))
                    # print("The played note is {}".format(played_note))
                    print(Note.logic.log_score())
                    self.inside_note = True
                if helpers.note_dict[self.note_with_octave] == helpers.note_dict[played_note]:
                    self.note_hit += 1
            else:
                if not self.finished_note:
                    self.note_hite_rate = self.note_hit / self.max_hits_per_note
                    # print("finished note {} with a hit rate of {}".format(self.note_with_octave, self.note_hite_rate))
                    print(Note.logic.log_score())
                    if self.note_hite_rate > 0.7:
                        self.image.fill((0,200,0))
                        Note.logic.hit_note()
                    else:
                        self.image.fill((200,0,0))
                        Note.logic.missed_note()
                    self.finished_note = True
                    

class NoteDecoration(pyg.sprite.Sprite):
    def __init__(self, index, parent_surface):
        pyg.sprite.Sprite.__init__(self)
        width = parent_surface.get_rect().width
        height = (parent_surface.get_rect().height / helpers.total_nb_notes)
        self.image = pyg.Surface([width, height])
        color = helpers.colors["NoteDecOn"] if index % 2 == 0 else helpers.colors["NoteDecOff"]
        self.image.fill(color)
        self.image.set_colorkey(color)
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = index * height
        print(index, ( self.rect.x, self.rect.y, width, height))

        pyg.draw.rect(self.image, color, [0, 0, width, height])