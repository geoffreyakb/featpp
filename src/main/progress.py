# Modules Python
import os
import csv
import sys
import importlib
import datetime

# Modules featpp
from Scenario import Scenario
from typeAnnotations import *
import utility

# Fichier stockant les paths utiles
from variables import *


def progress(tp, promo):

    tp = os.path.join(projects_path, tp)
    
    students = os.path.join(repository_path[promo], "students.csv")
    database_address = os.path.join(tp, "database_test.db")
    
    if not os.path.exists(tp) :
        print("Le chemin vers le TP est invalide. Opération avortée.\n")
        sys.exit(5)
    
    # Recuperation des scenarios instancies dans le fichier de configuration
    sys.path.append(tp)
    try :
        fichier_config = importlib.import_module("config")
    except ModuleNotFoundError:
        sys.path.remove(tp)
        print("\nFichier config.py non trouvé ou mal écrit. Opération avortée.")
        sys.exit(1)
    sys.path.remove(tp)
    
    try :
        # Liste des scenarios instancies dans le fichier de configuration
        scenarios = fichier_config.SCENARIOS
    except AttributeError:
        print("\nLa liste des scenarios \"SCENARIOS\" est absente dans config.py. Opération avortée.")
        sys.exit(2)
        
    # Vérification du "bon typage" des scenarios pour le bon fonctionnement des opérations ultérieures
    for sce in scenarios :
        if not isinstance(sce, Scenario) :
            print("Veuillez n'ajouter que des scénarios dans la liste SCENARIOS. Opération avortée.\n")
            sys.exit(6)
    
    # Recuperation des logins des etudiants depuis le fichier .csv passe en argument
    # Liste des logins des etudiants
    students_list = [] 
    try :
        with open(students, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            line_count = 1
            for row in reader:
                students_list.append(row["Students"])
                line_count += 1
    except OSError:
        print("\nListe des étudiants non trouvée. Opération avortée.")
        sys.exit(3)
    except :
        print("\nUne erreur est survenue pendant la lecture du fichier .csv")
        sys.exit(4)
    
    # Ecriture de l'avancée globale dans un fichier 
    text = utility.print_overall_progress(database_address, students_list, scenarios)
    date = str(datetime.datetime.today().strftime("%Y-%m-%d_%Hh%Mm%Ss"))
    with open(tp + '/avancee_globale_' + date + '.txt', 'w') as overall_progress:
        overall_progress.write(text)
        overall_progress.close()