from music21 import *
import unittest
from NN_preprocessing import new_preprocessing as preproc
import helper_fun as helper

class Test_musicLib(unittest.TestCase):
    scores = preproc.loadScores()

    def test_flattening_order(self):
        f_scores = []
        for score in self.scores:
            f_scores.append(score.flat.elements)

        for score, f_score in zip(self.scores, f_scores):
            pass


    def test_part_offset(self):

        control_list = helper.checkPartOffset(self.scores)
        for s_control in control_list:
            for element in s_control:
                if not element:
                    control_resulut = False
        control_result = True
        breakpoint()
        unittest.assertEqual(control_result, True)



if __name__ == '__main__':
    unittest.main()
