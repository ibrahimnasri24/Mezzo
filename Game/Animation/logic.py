from SheetMusic import import_xml
from Animation import sprites

class Logic:
    _instance = None
    max_missed_notes = 5

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.state = "main-menu"
            self.notes = []
            self.reset()

    @classmethod
    def get_instance(cls):
        Logic()
        return cls._instance
    
    
    def select_sheet(self, file_path, notes_container):
        self.notes = import_xml.xml_to_list(file_path)
        self.drawable_notes = sprites.Notes(notes_container, self.notes)
        self.state = "game-loop"
        
    def finished_score(self):
        self.state = "finished"
    
    def update_accuracy(self):
        self.played_notes += 1
        self.accuracy = (self.hit_notes / self.played_notes) * 100

    def hit_note(self):
        self.hit_notes += 1
        self.update_accuracy()

        self.cum_missed_notes = 0

    def missed_note(self):
        self.missed_notes+= 1
        self.update_accuracy()

        self.cum_missed_notes += 1

        if self.cum_missed_notes > Logic.max_missed_notes:
            self.gameover = True

    def reset(self):
        self.accuracy = 0

        self.played_notes = 0
        self.hit_notes = 0
        self.missed_notes = 0

        self.cum_missed_notes = 0

        self.gameover = False

    def log_score(self):
        return {"acc": self.accuracy, "hits": self.hit_notes, "misses": self.missed_notes, "cum":self.cum_missed_notes, "played":self.played_notes, "gameover": self.gameover}