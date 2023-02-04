import music21 as m21

noir_bpm = 120

def xml_to_list(xml):
    xml_data = m21.converter.parse(xml)
    score = []
    for part in xml_data.parts:
        for note in part.recurse().notesAndRests:
            measure = note.getContextByClass("Measure")
            if note.isRest:
                start = note.offset
                duration = note.quarterLength
                score.append({"start":start, "duration":duration, "note":"rest", "measure_Nb":measure.measureNumber})
            else:
                start = note.offset
                duration = note.quarterLength
                try:
                    noteNameWithOctave = note.nameWithOctave
                    score.append({"start":start, "duration":duration, "note":noteNameWithOctave, "measure_Nb":measure.measureNumber})
                except:
                    pass
    return score