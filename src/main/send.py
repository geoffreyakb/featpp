# Modules Python
import sys
import os
import csv
import datetime
import sqlite3
import importlib
import shutil
import subprocess
import traceback

# Modules Featpp
from Scenario import Scenario
from setup import make_path
from Tool import Tool
from typeAnnotations import *
import utility

# Fichier stockant les paths utiles
from variables import *

@argumentType("project", str)
@argumentType("promos", str)
def send(project, *promos):

    for eleves in promos:

        project_folder = os.path.join(projects_path, project)
        path_liste_eleves = os.path.join(repository_path[eleves], "students.csv")

        if not os.path.exists(project_folder) :
            print("Le chemin vers le TP est invalide. Opération avortée.\n")
            sys.exit(6)

        database_address = os.path.join(project_folder, "database_test.db")
        modalities_address = os.path.join(project_folder, "public", "modalites.txt")

        # Récupération des scénarios instanciés dans le fichier de configuration
        sys.path.append(project_folder)
        try :
            fichier_config = importlib.import_module("config")
        except ModuleNotFoundError:
            sys.path.remove(project_folder)
            print("Fichier config.py non trouvé ou mal écrit. Opération avortée.\n")
            sys.exit(1)
        sys.path.remove(project_folder)

        # Recuperation des scenarios instancies dans le fichier de configuration
        try :
            scenarios = fichier_config.SCENARIOS # Liste des scenarios instancies dans le fichier de configuration
        except AttributeError:
            print("La liste des scenarios \"SCENARIOS\" est absente dans config.py. Opération avortée.\n")
            sys.exit(2)

        # Recuperation de la liste des outils utilises
        #tools = Tool.tool_instances

        # TODO Vérification de l'existence de l'outil

        # TODO Vérification de la presence de l'outil

        # TODO Vérification que les outils sont opérationnels (selfchecks)
        #for tool in tools:
        #    tool.selfcheck(options)

        # Recuperation des logins des etudiants depuis le fichier .csv passe en argument
        students_list = [] # Liste des logins des etudiants
        try :
            with open(path_liste_eleves, mode='r') as liste_eleves:
                reader = csv.DictReader(liste_eleves)
                line_count = 1
                for row in reader:
                    students_list.append(row["Students"])
                    line_count += 1
        except OSError as e:
            print(f"Liste des étudiants non trouvée : {path_liste_eleves}\nOpération avortée.\n")
            sys.exit(3)
        except :
            print("Une erreur est survenue pendant la lecture du fichier csv. Opération avortée.\n")
            sys.exit(5)


        # Création d'une base de données contenant une table par scénario, chacune ayant une colonne par information persistente d'un scenario
        create_database(database_address, scenarios, students_list)
        
        # Création du fichier 'modalites.txt'
        modalities = open(modalities_address, 'w')
        modalities.write(utility.modalities_text(scenarios, database_address))
        modalities.close()
        
        # Création d'une variable d'environnement pour gérer l'identifiant des environnement isolés crées par isolate
        os.environ["ISOLATE_ID"] = "0"

        # Déploiement des fichiers dans le svn des élèves
        with open(path_liste_eleves, 'r') as liste_eleves:
            reader = csv.DictReader(liste_eleves)
            for row in reader:
                student = row["Students"]
                student_path = os.path.join(repository_path[eleves], student)

                existed = make_path(student_path)
                if existed == False:
                    svnAdd2 = f"svn add {student_path}"
                    subprocess.run(svnAdd2, shell=True)

                shutil.copytree(os.path.join(project_folder, 'public'), os.path.join(student_path, project))
                # Push la copie locale vers le serveur SVN
                svnAdd = "svn add " + os.path.join(student_path, project)
                subprocess.run(svnAdd, shell=True)
            svnCommit = f"svn commit -m 'Nouveau TP !' {repository_path[eleves]}"
            subprocess.run(svnCommit, shell=True)



def create_database(database_address, scenarios, students_list):
    
    """
        Cette fonction permet de créer la base de données à partir de la liste des
        étudiants et de la liste des scénarios.       

        Paramètres de la fonction :
            database_address : String - Chemin vers la base de données.
            scenarios : Scenario[] - Liste de tous les scénarios renseignés par l'enseignant 
                                     dans le fichier de configuration.
            students_list : String[] - Liste des identifiants des étudiants (ex : Paul Veyet -> pveyet)
    """

    if os.path.exists(database_address):
        os.remove(database_address)

    # Vérification du "bon typage" des scenarios pour le bon fonctionnement des opérations ultérieures
    for sce in scenarios :
        if not isinstance(sce, Scenario) :
            print("Veuillez n'ajouter que des scénarios dans la liste SCENARIOS. Opération avortée.\n")
            sys.exit(4)
    
    # Récupération des noms des scénarios déclarés dans le fichier de configuration
    tables = [scenarios[i].run.__name__ for i in range(len(scenarios))]

    # Création d'une base de données contenant une table par scénario, chacune ayant une colonne par information persistente d'un scenario
    con = sqlite3.connect(database_address)
    cur = con.cursor()
    for t in tables:
        cur.execute("CREATE TABLE " + t + " (Students"
                                            + ", Attempts" 
                                            + ", Date"
                                            + ", Mark" 
                                            + ", Penalty"
                                            + ", Attempts_Done"
                                            + ");")   
    
    # Complétion des tables des scénarios dans la base de données
    row = [""]*(len(tables))
    attempts = [str(scenarios[i].nb_attempts) for i in range(len(scenarios))]
    date = datetime.datetime.today()
    mark = "0"
    penalty = "0"
    attempts_done = "0"
    for k in range(len(tables)):
        row[k] = [(students_list[i], attempts[k], str(date), mark, penalty, attempts_done) for i in range(len(students_list))]
        cur.executemany("INSERT INTO " + tables[k] + " (Students" 
                                                    + ", Attempts" 
                                                    + ", Date"
                                                    + ", Mark" 
                                                    + ", Penalty"
                                                    + ", Attempts_Done"
                                                    + ") VALUES (?, ?, ?, ?, ?, ?);", row[k])
    
    con.commit()
    con.close()