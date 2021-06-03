import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
from main_progress import progress

class ProgressTest4(unittest.TestCase):
    
    def setUp(self):
        self.csv_path = env.PATH + '/tests/unitaires/main/test_files/students.csv'
        self.wrong_project_folder3 = env.PATH + '/tests/unitaires/main/wrong_folder3'
        
    def test_setup_config_not_ok(self):
        # Cas où le fichier de config a un nom différent
        with self.assertRaises(SystemExit) as cm:
            progress(self.wrong_project_folder3, self.csv_path)
        exception = cm.exception
        self.assertEqual(exception.code, 1)
    
if __name__ == '__main__':
    unittest.main(verbosity=2)