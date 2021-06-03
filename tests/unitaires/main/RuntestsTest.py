import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
from main_runtests import runtests

class RuntestsTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_runtests_OK(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)