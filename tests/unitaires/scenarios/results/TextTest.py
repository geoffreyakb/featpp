import unittest
import sys
import os

sys.path.append(sys.path[0] + "/../../../../")

import env
from Text import Text
from Result import Result




class TextTest(unittest.TestCase):

    def test_constructor_heritage(self):
        # -- Test qui vérifie si l'objet construit hérite bien de Result
        self.assertTrue(isinstance(Text("Titre de niveau 3", 3), Result))
    
    def test_constructor_error_less_than_zero(self):
        # -- Test qui vérifie que l'exception est levée pour < 0
        self.assertRaises(ValueError, Text, "Titre de niveau -1", -1)
    
    def test_constructor_error_more_than_six(self):
        # -- Test qui vérifie que l'exception est levée pour > 6
        self.assertRaises(ValueError, Text, "Titre de niveau 7", 7)

    def test_constructor_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans le constructeur
        self.assertRaises(TypeError, Text, 3, 3)
        self.assertRaises(TypeError, Text, "Texte", "Texte")

    def test_get_message_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans la fonction get_message
        text = Text("Error", 0)
        self.assertRaises(TypeError, text.get_message, "String")
        
    def test_get_message_level_zero(self):
        # -- Test avec un level à 0
        text = Text("Titre de niveau 0", 0)
        text_read = text.get_message(0)
        self.assertEqual(text_read, "Titre de niveau 0\n")
    
    def test_get_message_level_one(self):
        # -- Test avec un level à 1
        text = Text("Titre de niveau 1", 1)
        text_read = text.get_message(0)
        
        # Ce à quoi le texte est supposé ressembler
        text_lvl1 = ("\n\n###############################\n# " 
                    + "Titre de niveau 1" 
                    + "\n###############################\n\n")
        self.assertEqual(text_read, text_lvl1)
    
    def test_get_message_level_two(self):
        # -- Test avec un level à 2
        text = Text("Titre de niveau 2", 2)
        text_read = text.get_message(0)
        
        # Ce à quoi le texte est supposé ressembler
        text_lvl2 = ("\n\n===============================\n# " 
                    + "Titre de niveau 2" 
                    + "\n===============================\n\n")
        self.assertEqual(text_read, text_lvl2)
    
    def test_get_message_level_three(self):
        # -- Test avec un level à 3
        text = Text("Titre de niveau 3", 3)
        text_read = text.get_message(0)
        
        # Ce à quoi le texte est supposé ressembler
        text_lvl3 = ("\n\n-------------------------------\n# " 
                    + "Titre de niveau 3" 
                    + "\n-------------------------------\n\n")
        self.assertEqual(text_read, text_lvl3)
    
    def test_get_message_level_four(self):
        # -- Test avec un level à 4
        text = Text("Titre de niveau 4", 4)
        text_read = text.get_message(0)
        
        # Ce à quoi le texte est supposé ressembler
        text_lvl4 = ("\n\n" 
                    + "Titre de niveau 4" 
                    + "\n# # # # # # # # # # # # # # # #\n\n")
        self.assertEqual(text_read, text_lvl4)
    
    def test_get_message_level_five(self):
        # -- Test avec un level à 5
        text = Text("Titre de niveau 5", 5)
        text_read = text.get_message(0)
        
        # Ce à quoi le texte est supposé ressembler
        text_lvl5 = ("\n\n" 
                    + "Titre de niveau 5" 
                    + "\n= = = = = = = = = = = = = = = =\n\n")
        self.assertEqual(text_read, text_lvl5)
    
    def test_get_message_level_six(self):
        # -- Test avec un level à 6
        text = Text("Titre de niveau 6", 6)
        text_read = text.get_message(0)
        
        # Ce à quoi le texte est supposé ressembler
        text_lvl6 = ("\n\n" 
                    + "Titre de niveau 6" 
                    + "\n- - - - - - - - - - - - - - - -\n\n")
        self.assertEqual(text_read, text_lvl6)

if __name__ == '__main__':
    unittest.main(verbosity=2)