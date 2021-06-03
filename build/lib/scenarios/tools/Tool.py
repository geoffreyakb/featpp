from typeAnnotations import *
from Result import Result

class Tool() :

    """ 
        Classe abstraite rassemblant les caractéristiques communes a tous les outils 
        
        Paramètres du constructeur :
            _input : String - Le chemin vers le fichier d'entree de l'outil
            _output : String - Le chemin vers le fichier de sortie de l'outil 
    """
    
    tool_instances = []

    @argumentType("_command", str)
    def __init__(self, _command):
        self.command = _command
        Tool.tool_instances.append(self)

    def __repr__(self):

        """
            Affichage d'un outil lors d'un print
        """

        return self.command


    @returnType(Result)
    def run(self, project_env):

        """
            Lancement d'une exécution de l'outil sur un ou plusieurs fichiers
            
            Paramètres :
                files : liste de String - La liste des fichiers a passer dans l'outil
        """

        raise NotImplementedError()


    def selfcheck(self, options):

        """
            Lancement d'un test rapide de bon fonctionnement de l'outil
        """
        
        raise NotImplementedError()

@argumentType("arg1", str, True)
@argumentType("arg2", str, True)
@returnType(str, True)
def select_arg(arg1,arg2) :
            if arg1 != None :
                return arg1
            else : 
                return arg2