from Result import *
from typeAnnotations import *


class ToolResult(Result) :

    """ 
        Classe générique représentant le résultat d'un outil

        Paramètres du constructeur :
            _title : String - Message titre du résultat
            _result : String - Résultat même de l'outil (e.g "OK" ou "ERROR")
            _details : String - Détails d'execution de l'outil
            _mode: Int - Mode d'affichage du retour, plus ou moins détaillé
    """

    @argumentType("_title", str)
    @argumentType("_result", str)
    @argumentType("_details", str)
    def __init__(self, _title, _result, _details=""):
        Result.__init__(self, _result)
        self.title = _title
        self.details = _details


    @returnType(str)
    def get_message(self, mode = 1):
        message = self.title + " : " + self.result + "\n"

        if mode == 1 :
            message+= self.details

        return message