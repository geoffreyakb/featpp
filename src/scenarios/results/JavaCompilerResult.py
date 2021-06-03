from ToolResult import *
from typeAnnotations import *

class JavaCompilerResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par le compilateur Java

        Paramètres du constructeur :
            _filenames : String - Nom du fichier compilé
            _details : String - Détails d'execution de l'outil
            _test_compil : Bool - Booléen correspondant à si oui ou non la compilation a fonctionné
    """
    
    @argumentType("_filenames", {list :str})
    @argumentType("_details", str)
    @argumentType("_test_compil", bool)
    def __init__(self,_filenames, _details, _test_compil):
        title = "Compilation de " + ", ".join(_filenames)
        if _test_compil:      
            result = OK
        else:
            result  = FAILURE
        ToolResult.__init__(self, title, result, _details)
