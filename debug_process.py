import music21
import numpy as np
import sys
from NN_preprocessing import new_preprocessing as preproc
from NN_preprocessing import manipulate_score as sc

path ='./music_short/fav/'
score = preproc.loadScores(path)
#show sample food
#isStandard(food)
#print out to file ?
food = preproc.make_food(score)

inp,outp = food
inp = np.array(inp)
outp = np.array(outp)

food = inp,outp

def showSample(food):

    inp,outp = food
    print("WHOLE INPUT :\n\n ")
    print(inp)
    print("Song Sequences : \n\n")
    print(inp[0])
    print("Single Sequence : \n\n")
    print(inp[0][0])
    print("Object : \n\n")
    print(inp[0][0][0])


    return 0

showSample(food)

