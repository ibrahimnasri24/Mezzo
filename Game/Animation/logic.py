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
            self.reset_score()

    @classmethod
    def get_instance(cls):
        Logic()
        return cls._instance
    
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
            # self.reset_score()

    def reset_score(self):
        self.accuracy = 0

        self.played_notes = 0
        self.hit_notes = 0
        self.missed_notes = 0

        self.cum_missed_notes = 0

        self.gameover = False

    def log_score(self):
        return {"acc": self.accuracy, "hits": self.hit_notes, "misses": self.missed_notes, "cum":self.cum_missed_notes, "played":self.played_notes}