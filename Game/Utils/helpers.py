notes=[
    ("mi_0",    80),
    ("fa_0",    86),
    ("fa♯_0",   91.5),
    ("sol_0",   95),
    ("la♭_0",   102),
    ("la_0",    110),
    ("ci♭_0",   116),
    ("ci_0",    124),
    ("do_1",    130),
    ("do♯_1",   138),
    ("re_1",    145),
    ("mi♭_1",   153),
    ("mi_1",    162),
    ("fa_1",    172),
    ("fa♯_1",   180),
    ("sol_1",   192.5),
    ("la♭_1",   200.5),
    ("la_1",    215),
    ("ci♭_1",   228.5),
    ("ci_1",    242),
    ("do_2",    256),
    ("do♯_2",   273),
    ("re_2",    287),
    ("mi♭_2",   307),
    ("mi_2",    326),
    ("fa_2",    344.5),
    ("fa♯_2",   361),
    ("sol_2",   383),
    ("la♭_2",   401),
]


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