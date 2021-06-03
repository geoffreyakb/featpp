import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
from main_mill import mill

class MillTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_mill_OK(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)