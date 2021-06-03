import unittest
from typeAnnotations import *

class TypeAnnotationTest(unittest.TestCase):

    def testSimpleAnnotationOK(self):
        
        "Annote une fonction prenant un entier et renvoyant un string : vérification de la bonne exécution de la fonction"

        @argumentType("a", int)
        @returnType(str)
        def f(a):
            return "Bonjour"

        assert f(5) == "Bonjour"
    

    def testSimpleArgumentAnnotationKO(self):
            
        "Annote une fonction prenant un string et renvoyant un string : Passage d'un entier en paramètre"

        @argumentType("a", str)
        @returnType(str)
        def f(a):
            return "Bonjour"

        try:
            f(5)
            assert False
        except TypeError:
            assert True


    def testSimpleReturnAnnotationKO(self):
            
        "Annote une fonction prenant un string et renvoyant un int : Renvoi d'une chaine"

        @argumentType("a", int)
        @returnType(int)
        def f(a):
            return "Bonjour"

        try:
            f(5)
            assert False
        except TypeError:
            assert True

    def testDefaultAnnotationOK(self):
        
        "Annote une fonction prenant un entier facultatif : Pas d'argument renseigné"

        @argumentType("a", int)
        def f(a=2):
            return "Bonjour"

        assert f() == "Bonjour"


    def testDefaultWithPrecisionAnnotationOK(self):
        
        "Annote une fonction prenant un entier facultatif : Argument renseigné"

        @argumentType("a", int)
        def f(a=2):
            return "Bonjour"

        assert f(5) == "Bonjour"


    def testDefaultAnnotationCallKO(self):
        
        "Annote une fonction prenant un entier : Passage d'un string en argument"

        @argumentType("a", int)
        def f(a=2):
            return "Bonjour"

        try:
            f("Truc")
            assert False
        except TypeError:
            assert True


    def testDefaultAnnotationAppelOK(self):
        
        "Annote une fonction prenant un entier avec valeur par défaut string : Passage d'un entier en argument"

        @argumentType("a", int)
        def f(a="Salut"):
            return "Bonjour"

        assert f(2) == "Bonjour"


    def testClassType(self):
        
        "Annote une fonction prenant une classe en argument"

        class A():
            pass

        @argumentType("a", A)
        def f(a):
            return "Bonjour"

        assert f(A()) == "Bonjour"


    def testClassType(self):
        
        "Annote une fonction prenant une classe en argument : héritage"

        class A():
            pass

        class B(A):
            pass

        @argumentType("a", A)
        def f(a):
            return "Bonjour"

        assert f(B()) == "Bonjour"


    def testClassType(self):
        
        "Annote une fonction prenant une classe en argument : Autre classe sans héritage"

        class A():
            pass

        class B():
            pass

        @argumentType("a", A)
        def f(a):
            return "Bonjour"

        try:
            assert f(B()) == "Bonjour"
            assert False
        except TypeError:
            assert True

    def testComplexType(self):
        
        "Vérification de type complexe correct"

        @argumentType("a", {list: {list: {dict: (int, {list: (str, int)})}}})
        def f(a):
            return "Bonjour"

        assert f([[{4 : [("test", 3)], 5 : [("a", 1), ("b", 2)]}, {}], []]) == "Bonjour"


    def testSubComplexType(self):
        
        "Vérification de type complexe plus général correct"

        @argumentType("a", {list: {list: dict}})
        def f(a):
            return "Bonjour"

        assert f([[{4 : [("test", 3)], 5 : [("a", 1), ("b", 2)]}, {}], []]) == "Bonjour"


    def testComplexTypeKO(self):
        
        "Vérification de type complexe incorrect"

        @argumentType("a", {list: {list: {dict: (int, {list: (str, int)})}}})
        def f(a):
            return "Bonjour"

        try:
            f([[{4 : [("test", 3)], 5 : [("a", 1), (2, "b")]}, {}], []])
            assert False
        except TypeError:
            assert True


    def testNonableElement(self):
        
        "Vérification de type entier pouvant être None"

        @argumentType("a", int, True)
        def f(a):
            return "Bonjour"

        assert f(None) == "Bonjour"

    
    def testNonableDefaultElement(self):
        
        "Vérification de type entier pouvant être None par défaut"

        @argumentType("a", int, True)
        def f(a = None):
            return "Bonjour"

        assert f() == "Bonjour"

    
    def testNonableElement(self):
        
        "Vérification de type entier ne pouvant être None"

        @argumentType("a", int, False)
        def f(a):
            return "Bonjour"

        try:
            f(None)
            assert False
        except TypeError:
            assert True
            
    def testRecursiveNonableElement(self):
        
        "Vérification de type entier ne pouvant être None"

        @argumentType("a", {list: {list : int}}, True)
        def f(a):
            return "Bonjour"

        assert f([None]) == f([None, [2,None]])
