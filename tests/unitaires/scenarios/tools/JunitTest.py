import unittest
import sys

sys.path.append(sys.path[0] + "/../../../../")

import env
from Junit import Junit
from Tool import Tool
from ProjectEnv import ProjectEnv

class JunitTest(unittest.TestCase):

    def setUp(self):
        self.project_env = ProjectEnv(env.PATH + '/tests/unitaires/scenarios/tools', env.PATH + '/tests/unitaires/scenarios/tools')
        self.file_name = "junit_test_file.py"

    def test_constructor_heritage(self):
        # -- Test qui vérifie si l'objet construit hérite bien de Tool
        self.assertTrue(isinstance(Junit("command"), Tool))

    '''def test_run_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans la fonction run
        junit = Junit("command")
        self.assertRaises(TypeError, junit.run, 1, ["String"])
        self.assertRaises(TypeError, junit.run, ["String"], 2)'''
        
if __name__ == '__main__':
    unittest.main(verbosity=2)