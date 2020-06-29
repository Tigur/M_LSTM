from music21 import *

def midi_to_stateMat(midiFile):
    #It's matrix of states of each note
    score = converter.parse(midiFile)
    #print(score.flat.elements[0:50])
    set_of_tempos = set()
    list_of_tempos = list()
    print(len(score.flat))
    #score.flat.removeByClass('GeneralNote')
    score[0].removeByClass(tempo.MetronomeMark)
    #print(score[1][0])
    #print(len(score.flat))
    score[0].insert(0, tempo.MetronomeMark(number=160))
    for element in score.flat.elements :
        if not isinstance(element, note.GeneralNote) and not isinstance(element, note.Rest) and not isinstance(element, instrument.Instrument):# 
            #print(element.duration)
            # element.duration = duration.Duration(4.0)
            print(element)
            if isinstance(element, key.KeySignature)  :
                print("Above is Key signature! ")
                
            #set_of_tempos.add(element.number)
            #list_of_tempos.append(element.number)
    #print(set_of_tempos)
    #c = Counter(list_of_tempos)
    #print(c.most_common(1))
    #score.write('midi', fp = out_path)
    #new_score = converter.parse(out_path)
    #print(new_score)


