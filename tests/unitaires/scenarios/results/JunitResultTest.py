import unittest
import sys

sys.path.append(sys.path[0] + "/../../../../")

import env
from JunitResult import JunitResult
from ToolResult import ToolResult

class JunitResultTest(unittest.TestCase):

    def test_constructor_heritage(self):
        # -- Test qui vérifie si l'objet construit hérite bien de ToolResult
        self.assertTrue(isinstance(JunitResult("fichier.txt", "Details", True), ToolResult))
    
    def test_constructor_ok(self):
        # -- Test qui vérifie si on a bien le result à OK avec True
        compiler_result = JunitResult("fichier.txt", "Details", True)
        self.assertEqual(compiler_result.result, "OK")
    
    def test_constructor_error(self):
        # -- Test qui vérifie si on a bien le result à ERROR avec False
        compiler_result = JunitResult("fichier.txt", "Details", False)
        self.assertEqual(compiler_result.result, "ERROR")

    def test_constructor_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans le constructeur
        self.assertRaises(TypeError, JunitResult, 1, True, "String")
        self.assertRaises(TypeError, JunitResult, "String", 2, "String")
        self.assertRaises(TypeError, JunitResult, "String", True, 3)
if __name__ == '__main__':
    unittest.main(verbosity=2)