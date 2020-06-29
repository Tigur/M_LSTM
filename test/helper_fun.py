from music21 import *
from NN_preprocessing import options

def decapsulate(i,depth=1):
    while(depth > 0):
        i = i[0]
        depth = depth - 1
    return i




def loadTestOpt():
    options.fragment_len = 10
    options.fragment_number = 10
    options.longInput = True
    options.fragments = True
    options.binary = False

def custom_melody():
    food = []

    stream1 = stream.Stream()
    note1 = note.Note('C1', quarterLength=2.0)
    note2 = note.Note('D1', quarterLength=2.0)
    note3 = note.Note('E1', quarterLength=2.0)
    chord1 = chord.Chord(['C1','D1','E1'], quarterLength=2.0)
    tempo1 = tempo.MetronomeMark(number=120)
    metrum = meter.TimeSignature('3/4')

    stream1.append(tempo1)
    element = [-1,-1,3,tempo1.offset,120,0,0 ]
    food.append(element)
    stream1.append(metrum)
    element = [-1,-1,4,metrum.offset,120,metrum.numerator,metrum.denominator ]
    food.append(element)


    for _ in range(4):
        noteN = note.Note('C1', quarterLength=2.0)
        stream1.append(noteN)
        food.append([noteN.pitch.midi,noteN.quarterLength,0,noteN.offset,120,metrum.numerator,metrum.denominator])
        noteN = note.Note('C1', quarterLength=2.0)
        stream1.append(noteN)
        food.append([noteN.pitch.midi,noteN.quarterLength,0,noteN.offset,120,metrum.numerator,metrum.denominator])
        noteN = note.Note('C1', quarterLength=2.0)
        stream1.append(noteN)
        food.append([noteN.pitch.midi,noteN.quarterLength,0,noteN.offset,120,metrum.numerator,metrum.denominator])

    stream1.append(chord1)
    food.append([note1.pitch.midi,note1.quarterLength,0,chord1.offset,120,metrum.numerator,metrum.denominator])
    food.append([note2.pitch.midi,note2.quarterLength,0,chord1.offset,120,metrum.numerator,metrum.denominator])
    food.append([note3.pitch.midi,note3.quarterLength,0,chord1.offset,120,metrum.numerator,metrum.denominator])

    return [stream1], [food]

def isIdentical(f_score,score):
    for f_el, part in zip(f_score,score):
        pass

    return 0
def checkPartOffset(scores):
    all_offsets = []
    for score in scores:
        s_offsets = []
        for part in score.parts:
            s_offsets.append(part.offset)
        all_offsets.append(s_offsets)
    #check_list = [[True for part in s_offsets if len(s_offsets) == len(set(s_offsets))] for score in all_offsets]
    check_list = [[part for part in s_offsets if len(s_offsets) == len(tuple(s_offsets))] for score in all_offsets]

    breakpoint()

    return check_list

