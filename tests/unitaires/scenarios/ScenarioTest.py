import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
from Scenario import Scenario

class ScenarioTest(unittest.TestCase):
            
    def test_constructor_error_type_args(self):
        
        # -- Test les cas où on renseigne de mauvais types dans le constructeur
        self.assertRaises(TypeError, Scenario, 1, 0, 0, True, 0)
        self.assertRaises(TypeError, Scenario, useless_function, "2", 0, True, 0)
        self.assertRaises(TypeError, Scenario, useless_function, 0, "3", True, 0)
        self.assertRaises(TypeError, Scenario, useless_function, 0, 0, 4, 0)
        self.assertRaises(TypeError, Scenario, useless_function, 0, 0, True, "5")
        
    def test_get_name(self):
        scenario = Scenario(useless_function, -1, 0, True, 20)
        self.assertEqual(scenario.getName(), "useless_function")

def useless_function():
    return [ToolResult("Useless", "Function")]
         
if __name__ == '__main__':
    unittest.main(verbosity=2)