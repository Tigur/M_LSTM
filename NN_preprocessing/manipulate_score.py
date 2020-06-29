from collections import Counter
from music21 import *
from .m_classes import *
from formatting import *
from . import options
from collections.abc import Iterable
import sys
from . import MyExceptions as exc
#import options
import os

def flattened(score):
    score_flattened = stream.Score()
    for element in score.flat:
        score_flattened.append(element)

    return score_flattened


def removeClass(score,o_type):
    removed = []
    for element in score:
        if isinstance(element, o_type):
            removed.append(element)
            score.remove(element)

    return score

def split_chords(score):
    chord_offset = None
    #breakpoint()
    for object in score:
        if check_class(object) == MusicLabel.chord :
            #breakpoint()
            print(object.offset, "THIS IS OFFSET")
            chord_offset = object.offset
            chord = object
            try:
                score.remove(object)
                for note in chord.notes :
                    score.insert(float(chord_offset), note)
            except TypeError:
                print(f'{bcolors.FAIL}DUDE WE HAVE TYPE ERR !{bcolors.ENDC}')
                sys.exit("TYPE_ERROR")


    return score


def check_class(object):
    if isinstance(object, note.Note):
        return MusicLabel.note
    if isinstance(object, chord.Chord):
        return MusicLabel.chord
    if isinstance(object, note.Rest):
        return MusicLabel.rest
    if isinstance(object, tempo.MetronomeMark):
        return MusicLabel.tempo
    if isinstance(object, meter.TimeSignature):
        return MusicLabel.TimeSignature
    if isinstance(object, key.KeySignature):
        return MusicLabel.KeySignature
    else :
        return MusicLabel.other



    return 0



def simplify_tempo(score, one_tempo):
    """ Make score obliged to tempo """
    try:
        #breakpoint()
        score = flattened(score)
        #score = score.flat
    except:
        print(f"{bcolors.WARNING}WARN : CAN'T SIMPLIFY !!{bcolors.ENDC}", flush=True)

    finally:
       # breakpoint()
        full_len = len(score)
        tempo_count = [element for element in score.flat.elements if isinstance(element, tempo.MetronomeMark)]
        score = removeClass(score, type(tempo.MetronomeMark()))
        cut_len = len(score)
        if (full_len-cut_len)==len(tempo_count):
            print(str(full_len) + '-' + str(cut_len), full_len-cut_len, flush=True)
        else:
            print(f"{bcolors.FAIL}ERR : Funtion has trimed badly !!{bcolors.ENDC}", flush=True)
        if full_len-cut_len < options.fragment_len:

            raise MemoryError(f"{bcolors.FAIL}Score is too short after cut !!{bcolors.ENDC}")
        #breakpoint()
        score.insert(0,tempo.MetronomeMark(number=one_tempo.number))



        return score

def check_tempo(score):

    """ Return 5 most common tempos """
    # CAN DEFINITELY REDO THIS :
    # It is not entiely true that most common tempo is the best one to generalise.
    # to make it possible to adapt to different tempos in parts.


    all_tempos = [element for element in score.flat.elements if isinstance(element, tempo.MetronomeMark)]
    c = Counter(all_tempos)

    return c.most_common(5)

def presence_of(o_class, score):

    if o_class in score:
        return True
    else :
        return False

def isNeeded(object):
    pass


def get_new_info(score, bin_out = True):
    """
    Parses score flat info with tempo and TimeSignature.
    """
    tempo_list = []
    TimeSignature_list = []
    active_TimeSignature = (binary(0),binary(0))
    active_tempo = binary(0)
    active_TimeSignature_int = (0,0)
    active_tempo_int = -1

    for index,object in enumerate(score,0):
        if check_class(object) == MusicLabel.TimeSignature :

            active_TimeSignature = binary(object.numerator), binary(object.denominator)
            active_TimeSignature_int = object.numerator, object.denominator
        if check_class(object) == MusicLabel.tempo:
            active_tempo = binary(object.number)
            active_tempo_int = object.number

        if  options.binary :
            tempo_list.append(active_tempo)
            TimeSignature_list.append(active_TimeSignature)
        else :
            tempo_list.append(active_tempo_int)
            TimeSignature_list.append(active_TimeSignature_int)

    return TimeSignature_list, tempo_list

def existsIn(score, o_type):
    for element in score :
        if isinstance(element, o_type):
            return True
        if not isinstance(element,Iterable):
            return False
        else :
            for item in element:
                if isinstance(element, o_type):
                    return True
    return False


def prepare(score):
    """
    Transform score into multiDimentional list
    and simplify it's notation.
    """


    tempo = check_tempo(score)[0][0]
    #score = list(score.flat.elements)
    score = split_chords(score)
    try:
        score = simplify_tempo(score,tempo) # EXTERMINATS NOTES !!?
    except MemoryError:
        print(f"{bcolors.FAIL}Score is too short after cut !!{bcolors.ENDC}")
        #sys.exit()
    #breakpoint()
    #add_new_info(score)
    finally:#instead ELSE
        return score
