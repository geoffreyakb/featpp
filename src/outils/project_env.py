# Modules Python
import os

# Modules featpp
from typeAnnotations import *
from isolate import *

# Fichier qui stocke les paths utiles
from variables import *

class ProjectEnv():

    '''
    Cette classe contient les variables d'environnement utilisées tout au long de l'exécution du framework.
    
    Paramètres du constructeur :
        student_project_folder : String - Chemin du dossier du projet côté élève
        project_folder : String - Chemin du dossier du projet côté enseignant
        path_to_isolate_env : String - Le chemin absolu vers le répertoire isolé crée lors de l'initialisation de l'environement isolé
        isolate_id : String - L'identifiant (unique) de l'environement isolé définit lors de son initialisation
        sources_path : String -
    '''

    @argumentType("_student_project_folder", str)
    @argumentType("_project_folder", str)
    @argumentType("_path_to_isolate_env", str, True)
    @argumentType("_isolate_id", str, True)
    @argumentType("_sources_path", str)
    def __init__(self, _student_project_folder, _project_folder, _path_to_isolate_env = None, _isolate_id = None, _sources_path = "sources/"):
        
        self.student_project_folder = os.path.abspath(_student_project_folder) 
        self.project_folder = os.path.abspath(_project_folder)
        self.path_to_isolate_env = _path_to_isolate_env
        self.isolate_id = _isolate_id
        self.sources_path = _sources_path
        self.is_isolated = _path_to_isolate_env != None
        

    def move_sources(self):
        
        cp_state=isolate_mv(self.path_to_isolate_env, [self.student_project_folder + "/sources/*", self.project_folder + "/scriptsTests/*"])
        return cp_state.stdout