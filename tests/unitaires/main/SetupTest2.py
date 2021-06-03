import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
from main_setup import setup

class SetupTest(unittest.TestCase):
    
    def setUp(self):
        self.csv_path = env.PATH + '/tests/unitaires/main/test_files/students.csv'
        self.wrong_project_folder1 = env.PATH + '/tests/unitaires/main/wrong_folder1'
        
    def test_setup_config_scenarios_undefined(self):
        # Cas où on a un fichier de configuration où SCENARIOS est mal défini
        with self.assertRaises(SystemExit) as cm:
            setup(self.wrong_project_folder1, self.csv_path)
        exception = cm.exception
        self.assertEqual(exception.code, 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)