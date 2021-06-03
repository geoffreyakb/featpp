import unittest
import sys

sys.path.append(sys.path[0] + "/../../../../")

import env
from JavaCompiler import JavaCompiler
from Tool import Tool
from ProjectEnv import ProjectEnv

class JavaCompilerTest(unittest.TestCase):

    def setUp(self):
        self.project_env = ProjectEnv(env.PATH + '/tests/unitaires/scenarios/tools', env.PATH + '/tests/unitaires/scenarios/tools')
        self.file_name = "java_compiler_test_file.py"
        
    def test_constructor_heritage(self):
        # -- Test qui vérifie si l'objet construit hérite bien de Tool
        self.assertTrue(isinstance(JavaCompiler(), Tool))
        
    def test_constructor_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans la fonction run
        self.assertRaises(TypeError, JavaCompiler, 1, "String", "String")
        self.assertRaises(TypeError, JavaCompiler, "String", 2, "String")
        self.assertRaises(TypeError, JavaCompiler, "String", "String", 3)

    def test_run_error_type_args(self):
        # -- Test les cas où on renseigne de mauvais types dans la fonction run
        javacompiler = JavaCompiler()
        self.assertRaises(TypeError, javacompiler.run, 1, ["String"], "String", "String")
        self.assertRaises(TypeError, javacompiler.run, self.project_env, 2, "String", "String")
        self.assertRaises(TypeError, javacompiler.run, self.project_env, ["String"], "String", 3, "String")
        self.assertRaises(TypeError, javacompiler.run, self.project_env, ["String"], "String", "String", 4)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)