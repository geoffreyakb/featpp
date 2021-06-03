from typeAnnotations import *

OK = "OK"
FAILURE = "ERROR"

class Result() :

    """
    Classe abstraite représentant le résultat d'un run
    """

    def __init__(self, _result):
        self.result = _result

    @argumentType("dest_file", str)
    @argumentType("mode", int)
    @returnType(type(None))
    def print_result(self, dest_file, mode=0):

        """
        Etant de la classe Result, TextElement hérite de cette methode qui consiste à l'afficher selon son titleLVl
        """
        file_out = open(dest_file, "a")
        file_out.write(self.get_message(mode))
        file_out.close()

    @returnType(str)
    def get_message(self, mode = 1):
        raise NotImplementedError()
