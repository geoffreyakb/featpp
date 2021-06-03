# Modules Python
import importlib
import sqlite3
import datetime
import sys

# Modules featpp
from Scenario import Scenario
from ProjectEnv import ProjectEnv
from typeAnnotations import *
import utility

# Fichier stockant les paths utiles
from variables import *


@argumentType("promo", str)
@argumentType("student", str)
@argumentType("tp", str)
@returnType(type(None))
def evaluate(promo, student, tp, *scenarios_name) :

    '''
    Cycle d'execution manuelle des tests

    Paramètres :
        student - String : chemin relatif vers le dossier de l'étudiant contenant le projet
        tp - String : chemin relatif vers le dossier de l'enseignant contenant le projet
        *scenarios_name - List(String) : Liste de nom de scénarios à effectuer
    '''

    student_path = os.path.join(repository_path[promo], student)

    project_env = ProjectEnv(student_path,tp)
    #Definition de tous les chemins nécessaires à partir de l'environnement donné en argument
    student_project_folder = os.path.join(student_path, tp)
    project_folder = os.path.join(projects_path, tp)

    
    student_name = os.path.split(student_project_folder)[1]
    dest_address = os.path.join(project_folder, "public", "retours", "retour_manuel_", student_name+".txt")
    
    #Importation du fichier de configuration du projet
    sys.path.append(project_folder)
    fichier_config = importlib.import_module("config") # Import dynamique du fichier de configuration 
    sys.path.remove(project_folder)

    SCENARIOS = fichier_config.SCENARIOS

    #Selection des scenarios à jouer
    scenarios_to_run =[]
    for scenario in SCENARIOS :
        if scenario.run.__name__ in scenarios_name:
            scenarios_to_run.append(scenario)

    #Jouer les scénarios à jouer
    results = []
    for scenario in scenarios_to_run :
        results.append(scenario.run(project_env))
        
    #Afficher les résultats où il faut
    utility.print_results(results, dest_address , 2)