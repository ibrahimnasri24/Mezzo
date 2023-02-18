import os
import music21 as m21

noir_bpm = 80

def xml_to_list(xml):
    xml_data = m21.converter.parse(xml)
    score = []
    for part in xml_data.parts:
        for note in part.recurse().notesAndRests:
            measure = note.getContextByClass("Measure")
            if note.isRest:
                start = note.offset
                duration = note.quarterLength
                score.append({"start":start, "duration":duration, "note":"rest", "measure_Nb":measure.measureNumber, "tie": 'none'})
            else:
                start = note.offset
                duration = note.quarterLength
                tie = "none"
                if note.tie:
                    tie = note.tie.type
                try:
                    noteNameWithOctave = note.nameWithOctave
                    score.append({"start":start, "duration":duration, "note":noteNameWithOctave, "measure_Nb":measure.measureNumber, "tie": tie})
                except:
                    pass
    # for note in score:
    #     print(note)
    return score

def get_files_from_sheets_directory():
    sheets_dir = "Game/SheetMusic/SheetMusic"
    files = []

    for filename in os.listdir(sheets_dir):
        f = os.path.join(sheets_dir, filename)
        if os.path.isfile(f):
            if filename[-4:len(filename)] == ".xml":
                files.append({"path":f, "name":filename[0:-4]})

    return files