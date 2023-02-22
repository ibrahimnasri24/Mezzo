import pygame as pyg

colors = {
    "primary1": (200,200,200),
    "text1": (200,200,200),
    "background1": (50,50,50),
    "NoteDecOn": (90,90,90),
    "NoteDecOff": (60,60,60),
}

notes=[
    ("E2",    80),
    ("F2",    86),
    ("F#2",   91.5),
    ("G2",    95),
    ("A-2",   102),
    ("A2",    110),
    ("B-2",   116),
    ("B2",    124),
    ("C3",    130),
    ("C#3",   138),
    ("D3",    145),
    ("E-3",   153),
    ("E3",    162),
    ("F3",    172),
    ("F#3",   180),
    ("G3",    192.5),
    ("A-3",   200.5),
    ("A3",    215),
    ("B-3",   228.5),
    ("B3",    242),
    ("C4",    256),
    ("C#4",   273),
    ("D4",    287),
    ("E-4",   307),
    ("E4",    326),
    ("F4",    344.5),
    ("F#4",   361),
    ("G4",    383),
    ("A-4",   401),
]

notes_french={
    0:   "Mi",
    1:   "Fa",
    2:   "Fa♯",
    3:   "Sol",
    4:  "La♭",
    5:   "La",
    6:  "Ci♭",
    7:   "Ci",
    8:   "Do",
    9:   "Do♯",
    10:   "Re",
    11:  "Mi♭",
    12:   "Mi",
    13:   "Fa",
    14:  "Fa♯",
    15:   "Sol",
    16:  "La♭",
    17:   "La",
    18:  "Ci♭",
    19:   "Ci",
    20:   "Do",
    21:  "Do♯",
    22:   "Re",
    23:  "Mi♭",
    24:   "Mi",
    25:   "Fa",
    26:  "Fa♯",
    27:   "Sol",
    28:  "La♭",
    "none":  ""
}

total_nb_notes = 29

note_dict = {
    "E2":    0,
    "F-2":   1,
    "F2":    1,
    "F#2":   2,
    "G-2":   2,
    "G2":    3,
    "G#2":   4,
    "A-2":   4,
    "A2":    5,
    "B-2":   6,
    "B#2":   6,
    "B2":    7,
    "C-3":   7,
    "C3":    8,
    "C#3":   9,
    "D-3":   9,
    "D3":    10,
    "D#3":   11,
    "E-3":   11,
    "E3":    12,
    "E#3":   13,
    "F3":    13,
    "F#3":   14,
    "G-3":   14,
    "G3":    15,
    "G#3":   16,
    "A-3":   16,
    "A3":    17,
    "A#3":   18,
    "B-3":   18,
    "B3":    19,
    "C-4":   19,
    "B#4":   20,
    "C4":    20,
    "C#4":   21,
    "D-4":   21,
    "D4":    22,
    "D#4":   23,
    "E-4":   23,
    "E4":    24,
    "E#4":   25,
    "F-4":   25,
    "F4":    25,
    "F#4":   26,
    "G-4":   26,
    "G4":    27,
    "G#4":   28,
    "A-4":   28,
    "none":  "none",
}


def initialize_note_ranges():
    note_ranges = []
    for i, note in enumerate(notes):
        if i == 0:
            note_ranges.append({"note": note[0], "range":(note[1] - (abs(note[1] - notes[i + 1][1]) / 2), note[1] + (abs(note[1] - notes[i + 1][1]) / 2))})
        elif i == (len(notes) -1):
            note_ranges.append({"note": note[0], "range":(note[1] - (abs(note[1] - notes[i - 1][1]) / 2), note[1] + (abs(note[1] - notes[i - 1][1]) / 2))})
        else:
            note_ranges.append({"note": note[0], "range":(note[1] - (abs(note[1] - notes[i - 1][1]) / 2), note[1] + (abs(note[1] - notes[i + 1][1]) / 2))})
    return note_ranges



def extract_note_from_pitch(pitch, note_ranges):
    if pitch != 0:
        for i, note in enumerate(note_ranges):
            if pitch > note["range"][0] and pitch < note["range"][1]:
                return note["note"]
    return "none"



def text(string, color, bgcolor, size):
    font = pyg.font.Font('Game/Animation/assets/fonts/seguisym.ttf',size)
    text = font.render(string, True, color)
    return text