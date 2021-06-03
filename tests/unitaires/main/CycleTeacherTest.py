import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
from main_cycle_teacher import cycle_teacher

class CycleTeacherTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_cycle_teacher_OK(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)