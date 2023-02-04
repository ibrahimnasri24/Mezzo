import sys
import pygame as pyg
import multiprocessing
from PitchDetection import pitch_detector
from Animation import sprites
from Utils import helpers
from Animation import logic

class Animation:
    indicator_container_width = 250

    def __init__(self):
        pyg.init()
        self.FPSCLOCK = pyg.time.Clock()
        info = pyg.display.Info()
        self.screen = pyg.display.set_mode((0, 0), pyg.FULLSCREEN)
        self.width,self.height = info.current_w,info.current_h

        self.speed = [2, 2]
        self.black = 0, 0, 0

        self.indicator_container = pyg.Surface((Animation.indicator_container_width,self.height), pyg.SRCALPHA, 32)
        self.pitch_indicator = sprites.PitchIndicator(self.indicator_container)
        self.pitch_indicators = pyg.sprite.RenderPlain()
        self.pitch_indicators.add(self.pitch_indicator)

        self.notes_container = pyg.Surface((self.width,self.height))

        self.pitch = [0]

        self.logic = logic.Logic.get_instance()


    def draw_score(self):
        accuracy = helpers.text('Accuracy: {0:.3g}%'.format(self.logic.accuracy), helpers.colors["text1"], helpers.colors["background1"], 32)
        self.screen.blit(accuracy, (10, 10))



    def open_pitch_detector(self):
        self.pitch = multiprocessing.Array("d", 1)
        p2 = multiprocessing.Process(
                target=pitch_detector.main,
                args=(
                    self.pitch,
                ),
            )
        p2.start()

    def main_loop(self):
        self.note_ranges = helpers.initialize_note_ranges()

        notes = sprites.Notes(self.notes_container)

        while True:
            # print(helpers.extract_note_from_pitch(self.pitch[0], self.note_ranges))
            for event in pyg.event.get():
                if event.type == pyg.QUIT: sys.exit()

            self.screen.fill(self.black)


            notes.notes_container.fill((50,50,50))
            notes.update(helpers.extract_note_from_pitch(self.pitch[0], self.note_ranges))
            notes.notes.draw(self.notes_container)
            self.screen.blit(self.notes_container, (0, 0))


            self.indicator_container.fill((255,255,255, 150))
            self.pitch_indicator.update(helpers.extract_note_from_pitch(self.pitch[0], self.note_ranges))
            self.pitch_indicators.draw(self.indicator_container)
            self.screen.blit(self.indicator_container, (self.width - Animation.indicator_container_width, 0))
            
            self.draw_score()

            pyg.display.update()
            self.FPSCLOCK.tick(30)

    def start_anim(self):
        self.open_pitch_detector()
        self.main_loop()