import unittest
import sys
import os

sys.path.append(sys.path[0] + "/../../../../")

import env
from ToolResult import ToolResult
from Result import Result




class ToolResultTest(unittest.TestCase):
    
    def setUp(self):
        self.test_file_address = env.PATH + '/tests/unitaires/scenarios/results/test_file.txt'

    def test_constructor_heritage(self):
        # -- Test qui vérifie si l'objet construit hérite bien de Result
        self.assertTrue(isinstance(ToolResult("Title", "Result", "Details"), Result))

    def test_constructor_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans le constructeur
        self.assertRaises(TypeError, ToolResult, 1, "Result", "Details")
        self.assertRaises(TypeError, ToolResult, "Title", 2, "Details")
        self.assertRaises(TypeError, ToolResult, "Title", "Result", 3)

    def test_print_result_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans la fonctions
        text = ToolResult("Title", "Result", "Details")
        self.assertRaises(TypeError, text.print_result, 0, 0)
        self.assertRaises(TypeError, text.print_result, self.test_file_address, "Texte")
        
    def test_print_result_mode_zero(self):
        # -- Test avec un affichage synthétique
        open(self.test_file_address, 'w').close()
        text = ToolResult("Title", "Result", "Details")
        text.print_result(self.test_file_address, 0)
        
        # Ce à quoi le texte est supposé ressembler
        text_to_compare = "Title : Result\n"
        
        # Vérification de la bonne impression 
        file = open(self.test_file_address, 'r')
        text_read = file.read()
        file.close()
        self.assertEqual(text_read, text_to_compare)
        
        # Destruction du fichier créé
        os.remove(self.test_file_address)
        
    def test_print_result_mode_one(self):
        # -- Test avec un affichage détaillé
        open(self.test_file_address, 'w').close()
        text = ToolResult("Title", "Result", "Details")
        text.print_result(self.test_file_address, 1)
        
        # Ce à quoi le texte est supposé ressembler
        text_to_compare = "Title : Result\nDetails"
        
        # Vérification de la bonne impression 
        file = open(self.test_file_address, 'r')
        text_read = file.read()
        file.close()
        self.assertEqual(text_read, text_to_compare)
        
        # Destruction du fichier créé
        os.remove(self.test_file_address)

if __name__ == '__main__':
    unittest.main(verbosity=2)