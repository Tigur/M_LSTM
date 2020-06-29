import numpy as np
from NN_preprocessing import manipulate_score as pieces
from NN_preprocessing.m_classes import *
from NN_preprocessing import new_preprocessing as newp

def give_shapes():

    return i.shape,o.shape

def decapsulate(i,depth=1):
    while(depth > 0):
        i = i[0]
        depth = depth - 1
    return i

def look_for( scores, class_num):
    o_class = class_num
    for score in scores:
        score = score.flat.elements
        for element in score:
            if pieces.check_class(element) == o_class :
                return True
            else:
                return False
def isNormalised(food,div):
    for frag in food:
        for obj in frag:
            for element in enumerate(obj):
                if not element<=1 and element>=-1:
                    print("ERROR !! NOT NORMALISED !")
                    return False
    return True
# print(give_shapes())
# print(decapsulate(np.array(i),1))
#
# print("WHOLE : ")
# division = newp.normalisation_division(scores)
#
# print(look_for(scores,3))
# for i in range(6):
#     print(division[i][-1])
