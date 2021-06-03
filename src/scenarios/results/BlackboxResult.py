from ToolResult import *
from typeAnnotations import *

class BlackboxResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par le compilateur Java

        Paramètres du constructeur :
            _filenames : String - Nom du fichier compilé
            _details : String - Détails d'execution de l'outil
            _test_compil : Bool - Booléen correspondant à si oui ou non la compilation a fonctionné
    """
    
    @argumentType("_filename", str)
    @argumentType("_test_diff", bool)
    @argumentType("details", str)
    def __init__(self, _filename, _test_diff, details):
        title = "Test en boite noire de " + _filename
        if _test_diff:      
            result = OK
        else:
            result  = FAILURE
        
        ToolResult.__init__(self, title, result, details)
