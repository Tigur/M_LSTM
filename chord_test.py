from music21 import *

test_path = '/home/resolution/POważne_sprawy/studyjne/PRACA_INŻ/test_workspace/Chord_test.mid'

score = stream.Stream()
pitches = ['A1','C1','D1','D5','C5']

for pitch in pitches:
    n = note.Note(pitch)
    d = duration.Duration()
    d.quarterLength = 2
    n.duration = d
    score.insert(0, n)


#score.insert(1, note.Note('E5'))
score.insert(0, meter.TimeSignature('8/2'))

chordy = chord.Chord(['A5','C3','G2'])
chordy[2].offset = 3

score.insert(3, chordy)

print(score.flat.elements)

print(score.flat.elements[-1].notes[2].offset)
score.write('midi', fp = test_path)
