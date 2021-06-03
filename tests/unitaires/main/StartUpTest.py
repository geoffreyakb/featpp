import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
from main_start_up import start_up

class StartUpTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_start_up_OK(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)