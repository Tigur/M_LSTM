

from music21 import *

from collections import Counter
import numpy as np
import enum
import random
from . import options
from .m_classes import *
from .manipulate_score import *
import os
import pdb
import itertools
from misc import *
import sys
from formatting import binary




out_path = './t_output/test.mid'

def normalisation_division(scores):
    option = options.fragments
    options.fragments = False

    division = []

    pitches = []
    durations = []
    tempos = []
    met_numerator = []
    met_denominator = []
    offsets = []
    #food = make_food(scores)
    for index,score in enumerate(scores) :
        score = prepare(score)
        print('   >>>>  '+ str(index))
        for obj in score :
            o_class = check_class(obj)
            if o_class == MusicLabel.note:
                pitches.append(obj.pitch.midi)
            if o_class == MusicLabel.rest or MusicLabel.note:
                durations.append(float(obj.duration.quarterLength))
            offsets.append(obj.offset)
            if o_class == MusicLabel.tempo:
                tempos.append(obj.number)
            if o_class == MusicLabel.TimeSignature:
                met_numerator.append(obj.numerator)
                met_denominator.append(obj.denominator)
            #print(obj)
        #breakpoint()
        pitches = [max(pitches)]
        durations = [max(durations)]
        offsets = [max(offsets)]
        tempos = [max(tempos)]
        met_numerator = [max(met_numerator)]
        met_denominator = [max(met_denominator)]

    division = []
    division.append(pitches)
    division.append(durations)
    division.append([MusicLabel.other.value])
    division.append(offsets)
    division.append(tempos)
    division.append(met_numerator)
    division.append(met_denominator)

    for l in division:
        l.sort()
    options.fragments = True

    division = [item for sublist in division for item in sublist] # FLATTENING
    return division



def getRandomFragment(score):
    start = None
    #pdb.set_trace()
    max_start = len(score) - options.fragment_len - 1

    if max_start<=0:
        print("WRONG max_start !!", "Check the values !")
        pdb.set_trace()
        # the max_start eq is below 0 as the Fragment_len is 100

    while  start == None or start > max_start :
        start = random.randint(0,max_start)

    fragment = score[start:start+options.fragment_len]
    out_frag = score[start+1:start+options.fragment_len+1]

    return fragment, out_frag[-1]

def getFragmentSet(score):
    inSet = []
    outSet = []
    fragmentSet = [getRandomFragment(score) for fragment in range(options.fragment_number)]
    for fragment_pair in fragmentSet:
       inSet.append(fragment_pair[0])
       outSet.append(fragment_pair[1])
    return inSet, outSet

def object_to_food(object):
    #pdb.post_mortem()

    pitch = -1
    duration = -1
    o_class = None
    offset = None
    tempo_one = -1
    TimeSignature = (0,0)

    offset = object.offset
    o_class = check_class(object).value
    if isinstance(object, note.GeneralNote):
        duration = float(object.duration.quarterLength) #* 100
    if isinstance(object, note.Note):
        pitch = object.pitch.midi
    if isinstance(object, tempo.MetronomeMark):
        tempo_one = object.number
    if isinstance(object, meter.TimeSignature):
        TSig_n = object.numerator
        TSig_d = object.denominator

    if options.binary :
        input_list = [binary(pitch), binary(duration), binary(o_class), binary(offset)]
    else:
        input_list = [pitch, duration, o_class, offset]
        #print(duration)
    return input_list

def randomNote(rangeList):
    pitch = random.randint(0,rangeList[0])/rangeList[0] #randInt in range
    duration = random.randint(0,int(rangeList[1]))/rangeList[1] # randInt in range
    o_class = int(random.randint(0,rangeList[2])/rangeList[2])
    offset = random.randint(0,int(rangeList[3]))/rangeList[3]
    #tempo_one = random.randint(0,int(rangeList[4])) #randInt in range
    #TSig_n = random.randint(0,rangeList[5]) #randInt in range
    #TSig_d = random.randint(0,rangeList[6]) #randInt in range

    randNote = [pitch,duration,o_class,offset]
    return randNote
def randomSeq(rangeList):
    tempo_one = random.randint(0,int(rangeList[4]))/rangeList[4] #randInt in range
    TSig_n = int(random.randint(0,rangeList[5])/rangeList[5]) #randInt in range
    TSig_d = int(random.randint(0,rangeList[6])/rangeList[6]) #randInt in range
    sequence = []

    for _ in range(options.fragment_len):
        note = randomNote(rangeList)
        note.append(tempo_one)
        note.append(TSig_n)
        note.append(TSig_d)
        sequence.append(note)
    return sequence

def fragment_to_food(fragment) :

    ret = [object_to_food(object) for object in fragment]

    return ret

def getFoodPack(score):
    """ Forms a food Pack.
    One pack contains of multiple fragments of food
    First forms a rawPack and then transforms it to food pack
    """

    #score = score.flat # check if it will work
    #split_chords(score)
    #tempo = check_tempo(score)[0][0]
    #simplify_tempo(score,tempo)

    score = prepare(score)


    rawPack = [getRandomFragment(score) for element in range(options.fragment_number)]
    foodPack = [fragment_to_food(fragment) for fragment in rawPack]

    return foodPack

def getLongFood(score):
    #pdb.set_trace()
    score = prepare(score)
    #score = score.flat.elements
   # split_chords(score)
    food = []
    TimeSignature, tempo = get_new_info(score, bin_out=False)
    for index, object in enumerate(score,0) :

        food.append(object_to_food(object))
        food[index].append(tempo[index])

        food[index].append(TimeSignature[index][0])
        food[index].append(TimeSignature[index][1])
        #food[index] = normalise_obj(food[index])




    if options.fragments :
        food, out = getFragmentSet(food)
        food = np.array(food)
        out = np.array(out)

        return food,out
    return food

def make_food(scores):
    #pdb.set_trace()
    """
    scores - A list of all paths to midiFiles.
    """
#find_divisions(scores)

    div = normalisation_division(scores)

    if options.longInput :
        if options.fragments :
            food = [getLongFood(score)[0] for score in scores]
            out = [getLongFood(score)[1] for score in scores]
            print("Tu JEST MAKEFOOD")
            print(len(food))

          # food = list(itertools.chain.from_iterable(food))
          # out = list(itertools.chain.from_iterable(out))
            food = list(itertools.chain.from_iterable(food))
            out = list(itertools.chain.from_iterable(out))
# ---------------------------------------------------------------
            # for frag in food:
            #     for obj in frag:
            #         tmp = np.copy(obj)#DEBUG VAR
            #         for index,division in enumerate(div):
            #             obj[index] = obj[index]/division
            #             if obj[index] > 1 :

            #                 pdb.set_trace()
#-----------------------------------------------------------------
        else:
            food = [getLongFood(score)[:-1:] for score in scores]
            out = [getLongFood(score)[1::] for score in scores]

          # food = list(itertools.chain.from_iterable(food))
          # out = list(itertools.chain.from_iterable(out))
          #  food = list(itertools.chain.from_iterable(food))
          #  out = list(itertools.chain.from_iterable(out))


        return food,out



    else:
        for score in scores :

            print("Packed Food !!! ")

            getFoodPack(score)

        return None

def normalise_food(food,div):

    for frag in food:
        for obj in frag:
            tmp = np.copy(obj)
            for index,division in enumerate(div):
                obj[index] = obj[index]/division
                if obj[index] > 1 :
                    print(f"{bcolors.FAIL}NORMALISATION FAILED : FOOD{bcolors.ENDC}")
                    pdb.set_trace()
    return food

def normalise_out(out,div):

    for obj in out:
        tmp = np.copy(obj)
        for index,division in enumerate(div):
            obj[index] = obj[index]/division
            if obj[index] > 1 :
                print(f"{bcolors.FAIL}NORMALISATION FAILED: OUT{bcolors.ENDC}")
                pdb.set_trace()
    #breakpoint()
    return out



def loadScores(dirpath = '/home/resolution/POważne_sprawy/studyjne/PRACA_INŻ/Inż_repo/MUSIC_PACKAGE/'):
    count = 0
    current = 0
    scores = []
    for fname in os.listdir(dirpath):
        if fname[-4:] not in ('.mid','.MID'):
            continue

        count = count+1

    for fname in os.listdir(dirpath):
        if fname[-4:] not in ('.mid','.MID'):
            continue

        name = fname[:-4]
        current_path = dirpath + fname
        scores.append(converter.parse(current_path))

        current = current+1
        print("Loaded {} {}/{}".format(name,current,count))

    return scores

def obtain_init(sc_dir = './music_short/fav/'):
    scores = loadScores(sc_dir)
    i,o = make_food(scores)
    i = np.array(i)

    return i
def denormalize(vect,div):

    #breakpoint()
    for index,val in enumerate(vect):
        vect[index] = val*div[index]
    return vect

def pick_closest_class(val):
    all_list = [val,MusicLabel.note.value,MusicLabel.rest.value,MusicLabel.tempo.value,MusicLabel.TimeSignature.value]
    all_list.sort()

    v_ind = all_list.index(val)
    if v_ind == len(all_list)-1:
        val = all_list[v_ind-1]

    if (all_list[v_ind+1] - all_list[v_ind]) >= (all_list[v_ind] - all_list[v_ind-1]):
        val = all_list[v_ind-1]

    else:
        val = all_list[v_ind+1]

    return val
def vect_to_music(vect,div):
    vect = denormalize(vect,div)
    vect[2] = int(vect[2])
    vect[2] = pick_closest_class(vect[2])

    print(vect[2])
    #breakpoint()

    if vect[2]==MusicLabel.note.value:
        music_obj = note.Note()
        music_obj.pitch.midi = vect[0]
        music_obj.duration.quarterLength = vect[1]
        music_obj.offset = vect[3]
    if vect[2]==MusicLabel.rest.value:
        music_obj = note.Rest()
        music_obj.duration.quarterLength = vect[1]
        music_obj.offset = vect[3]
    if vect[2]==MusicLabel.tempo.value:
        music_obj = tempo.MetronomeMark()
        music_obj.number = vect[4]
        music_obj.offset = vect[3]
    if vect[2]==MusicLabel.TimeSignature.value:
        music_obj = meter.TimeSignature()
        music_obj.numerator = int(vect[5])
        music_obj.denumerator = int(vect[6])
        music_obj.offset = vect[3]
    if vect[2]==MusicLabel.KeySignature.value:
        music_obj = key.KeySignature()

    return music_obj

def conv_to_music(prediction,div):
    pred_score = stream.Score()
    for num_obj in prediction:
        music_obj = vect_to_music(num_obj,div)
        pred_score.append(music_obj)

    return pred_score

if __name__ == '__main__':

    rel_path = '/home/resolution/POważne_sprawy/studyjne/PRACA_INŻ/Inż_repo/MUSIC_PACKAGE/fav/'

    midiFile = rel_path + 'islamei.mid'
#    midi_to_stateMat(midiFile)
    print(midiFile)

