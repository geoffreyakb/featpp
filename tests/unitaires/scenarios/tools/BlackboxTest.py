import unittest
import sys

sys.path.append(sys.path[0] + "/../../../../")

import env
from Blackbox import Blackbox
from ProjectEnv import ProjectEnv

class BlackboxTest(unittest.TestCase):
    def setUp(self):
        self.project_env = ProjectEnv(env.PATH + '/tests/unitaires/scenarios/tools', env.PATH + '/tests/unitaires/scenarios/tools')
        self.file_name = "blackbox_test_file.py"

    def test_run_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans la fonction run
        blackbox = Blackbox()
        self.assertRaises(TypeError, blackbox.run, 1, "String")
        self.assertRaises(TypeError, blackbox.run, self.project_env, 2)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)