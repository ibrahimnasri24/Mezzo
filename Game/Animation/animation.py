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
        
        
        self.notes_container = pyg.Surface((self.width,self.height), pyg.SRCALPHA, 32)


        self.note_decorations_container = pyg.Surface((self.width,self.height))
        self.note_decorations = pyg.sprite.RenderPlain()
        for i, note in enumerate(reversed(helpers.notes)):
            note_dec = sprites.NoteDecoration(i, note, self.note_decorations_container)
            self.note_decorations.add(note_dec)

        self.pitch = [0]

        self.logic = logic.Logic.get_instance()


    def draw_score(self):
        accuracy = helpers.text('Accuracy: {0:.3g}%'.format(self.logic.accuracy), helpers.colors["text1"], helpers.colors["background1"], 32)
        self.screen.blit(accuracy, (150, 38))



    def open_pitch_detector(self):
        self.pitch = multiprocessing.Array("d", 2)
        self.pitch[0] = 0
        self.pitch[1] = 1
        self.p2 = multiprocessing.Process(
                target=pitch_detector.main,
                args=(
                    self.pitch,
                ),
            )
        self.p2.start()


    def draw_game_over_screen(self):
        gameover = helpers.text('GAME OVER', helpers.colors["text1"], helpers.colors["background1"], 64)
        gameover_rect = gameover.get_rect()
        self.screen.blit(gameover, ((self.width / 2) - (gameover_rect.width / 2), (self.height / 2) - (gameover_rect.height / 2)))

    
    def draw_currently_played_note(self):
        cur_played_note_text = helpers.text("Played Note: " + helpers.extract_note_from_pitch(self.pitch[0], self.note_ranges), helpers.colors["text1"], helpers.colors["background1"], 32)
        # cur_played_note_text_rect = cur_played_note_text.get_rect()
        self.screen.blit(cur_played_note_text, (440,38))


    def main_loop(self):
        self.note_ranges = helpers.initialize_note_ranges()

        notes = sprites.Notes(self.notes_container)

        running = True

        while running:
            # print(helpers.extract_note_from_pitch(self.pitch[0], self.note_ranges))
            for event in pyg.event.get():
                if event.type == pyg.QUIT: sys.exit()
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE or event.key == pyg.K_q:
                        print("exiting")
                        self.pitch[1] = 0
                        self.p2.join()
                        running = False
                        pyg.QUIT: sys.exit()
                    elif self.logic.gameover:
                        self.logic.reset()
                        self.notes_container = pyg.Surface((self.width,self.height), pyg.SRCALPHA, 32)
                        notes = sprites.Notes(self.notes_container)

            self.screen.fill((50,50,50))


            if self.logic.gameover:
                self.draw_game_over_screen()
            else:

                self.note_decorations_container.fill((50,50,50))
                self.note_decorations.update()
                self.note_decorations.draw(self.note_decorations_container)
                self.screen.blit(self.note_decorations_container, (0,0))
                
                notes.notes_container.fill((0,255,0,0))
                notes.update(helpers.extract_note_from_pitch(self.pitch[0], self.note_ranges))
                notes.notes.draw(self.notes_container)
                self.screen.blit(self.notes_container, (0, 0))

                self.indicator_container.fill((255,255,255,50))
                self.pitch_indicator.update(helpers.extract_note_from_pitch(self.pitch[0], self.note_ranges))
                self.pitch_indicators.draw(self.indicator_container)
                self.screen.blit(self.indicator_container, (self.width - Animation.indicator_container_width, 0))
                
                self.draw_currently_played_note()
                self.draw_score()

            pyg.display.update()
            self.FPSCLOCK.tick(30)

    def start_anim(self):
        self.open_pitch_detector()
        self.main_loop()