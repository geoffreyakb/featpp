import unittest
import sys
import os

sys.path.append(sys.path[0] + "/../../../../")

import env
from Penalty import Penalty
from Result import Result




class PenaltyTest(unittest.TestCase):

    def test_constructor_heritage(self):
        # -- Test qui vérifie si l'objet construit hérite bien de Result
        self.assertTrue(isinstance(Penalty("", 1), Result))

    def test_constructor_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans le constructeur
        self.assertRaises(TypeError, Penalty, 3, 3)
        self.assertRaises(TypeError, Penalty, "Penalty", "Penalty")

    def test_get_message_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans la fonction get_message
        penalty = Penalty("Error", 0)
        self.assertRaises(TypeError, penalty.get_message, "String")
        
    def test_get_message_ok(self):
        # -- Test que get_message fonctionne
        penalty = Penalty("Pénalité de 1 point", 1)
        self.assertEqual(penalty.get_message(), "Pénalité de 1 point\n")



if __name__ == '__main__':
    unittest.main(verbosity=2)