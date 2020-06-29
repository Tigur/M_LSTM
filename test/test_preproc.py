from NN_preprocessing import new_preprocessing as prep
import unittest
from NN_preprocessing import options
from music21 import *
import helper_fun as misc

    # Here you just Check if list made directly as [pitchN1,durationN1 etc. ... ] is the same as the product od make_food(score=stream)


class Test_new_preproc(unittest.TestCase):
    scores, expected_food =  misc.custom_melody()
    def test_make_food(self):
        longFood = []
        misc.loadTestOpt()
        fragFood = prep.make_food(self.scores)
        options.fragments = False
        longFood = prep.make_food(self.scores)
        longFood[0][0].append(longFood[1][0][-1])
        print(longFood[0])
        print('\n\n\n\n')
        print(self.expected_food)

        self.assertEqual(longFood[0], self.expected_food)

    def test_div(self):
        div = prep.normalisation_division(self.scores)

        print(div)
if __name__ == '__main__':
    unittest.main()
