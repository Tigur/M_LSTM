from NN_preprocessing import manipulate_score as sc
from music21 import *
import unittest
import helper_fun as misc


class Test_manipulate_score(unittest.TestCase):

    score,food = misc.custom_melody()
    def test_existsIn(self):
        self.assertEqual(sc.existsIn(self.score,type(note.Note())), True)
        self.assertEqual(sc.existsIn(self.score,type(chord.Chord())), False)
        self.assertEqual(sc.existsIn(self.score,type(rest.Rest())), False)

    def test_flattened(self):
        a = note.Note('A5')
        b = note.Note('B5')
        c = note.Note('C5')
        d = note.Note('D5')

        p_score = stream.Score()
        f_score = stream.Score()


        p_score.append(stream.Part())
        p_score.append(stream.Part())
        p_score[1].offset = 1.0


        notes = [a,b,c,d]
        for index,a_note in enumerate(notes):
            f_score.append(a_note)
            if index < 3:
                p_score[0].append(a_note)
            else:
                p_score[1].append(a_note)

        #breakpoint()

        ap_score = sc.flattened(p_score)
        #breakpoint()
        self.assertEqual(f_score.elements,ap_score.flat.elements)
        self.assertEqual(ap_score,p_score.flat.elements)




if __name__ == '__main__':
    unittest.main()
