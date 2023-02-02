import sys
import pygame as pyg
import multiprocessing
from PitchDetection import pitch_detector
from Animation import sprites

class Animation:
    def __init__(self):
        pyg.init()
        self.FPSCLOCK = pyg.time.Clock()
        info = pyg.display.Info()
        self.screen = pyg.display.set_mode((0, 0), pyg.FULLSCREEN)
        self.width,self.height = info.current_w,info.current_h

        self.speed = [2, 2]
        self.black = 0, 0, 0

        self.indicator_container = pyg.Surface((100,self.height))
        self.pitch_indicator = sprites.PitchIndicator(self.indicator_container)
        self.pitch_indicators = pyg.sprite.RenderPlain()
        self.pitch_indicators.add(self.pitch_indicator)

        self.pitch = [0]


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
        while True:
            print(self.pitch[0])
            for event in pyg.event.get():
                if event.type == pyg.QUIT: sys.exit()

            self.screen.fill(self.black)
            self.indicator_container.fill((255,255,255))

            self.pitch_indicator.update(self.pitch[0], 500, 50)
            self.pitch_indicators.draw(self.indicator_container)
            self.screen.blit(self.indicator_container, (self.width - 100, 0))

            pyg.display.update()
            self.FPSCLOCK.tick(60)

    def start_anim(self):
        self.open_pitch_detector()
        self.main_loop()