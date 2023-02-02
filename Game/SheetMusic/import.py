import music21 as m21

file_name = "Game/SheetMusic/TestSheets/test.xml"
def xml_to_list(xml):
    xml_data = m21.converter.parse(xml)
    score = []
    for part in xml_data.parts:
        for note in part.recurse().notesAndRests:
            if note.isRest:
                start = note.offset
                duration = note.quarterLength
                score.append([start, duration, -1])
            else:
                start = note.offset
                duration = note.quarterLength
                try:
                    pitch = note.nameWithOctave
                    pitchPS = note.pitch.ps
                    score.append([start, duration, pitch])
                except:
                    pass
    return score

print(xml_to_list(file_name))