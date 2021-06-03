import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
import main

class MainTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_main_OK(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)