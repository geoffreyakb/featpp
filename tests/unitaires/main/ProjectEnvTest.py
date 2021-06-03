import unittest
import sys
from jinja2.utils import pformat

sys.path.append(sys.path[0] + "/../../../")

import env
from ProjectEnv import ProjectEnv

class ProjectEnvTest(unittest.TestCase):

    def test_constructor_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans le constructeur
        self.assertRaises(TypeError, ProjectEnv, 1,"String", "String")
        self.assertRaises(TypeError, ProjectEnv, "String", 2, "String")
        self.assertRaises(TypeError, ProjectEnv, "String", "String", 3)

    def test_create_object_ok(self):
        # -- Test pour créer un objet
        spf = env.PATH + 'tests/main/test_files' 
        pf = env.PATH + 'tests/main/test_files2'
        pe = ProjectEnv(spf, pf)
        self.assertTrue(isinstance(pe,ProjectEnv))
    
if __name__ == '__main__':
    unittest.main(verbosity=2)