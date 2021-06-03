# Modules Python
import importlib
import sqlite3
import datetime
import os
import sys
import functools

# Modules featpp
import utility
from Scenario import Scenario
from ProjectEnv import ProjectEnv
from Penalty import Penalty
from typeAnnotations import *

# Fichier stockant les paths utiles
from variables import *

class WrongTestConfigurationException(Exception):
    '''
    Exception créée pour traiter le cas d'un fichier de configuration des tests compromis.
    '''
    pass

@argumentType("project", str)
@returnType(type(None))
def runtests(project):

    test_folder = os.path.join(projects_path, project, "testsProject")

    # Importation du fichier de configuration pour le projet concerné
    sys.path.append(test_folder)
    tst = importlib.import_module("tests_runner") # Importation de la variable TESTS
    sys.path.remove(test_folder)

    sys.path.append(os.path.join(projects_path, project))
    conf = importlib.import_module("config") # Importation de la variabel SCENARIO_TESTS
    sys.path.remove(os.path.join(projects_path, project))

    scs = {}
    for s in conf.SCENARIOS_TESTS:
        scs[s.getName()] = s

    def exec_scenar(folder, sc, has_to_be_ok):
        project_env = ProjectEnv(folder, project, _sources_path='')
        result = sc.run(project_env)
        return (functools.reduce(
            lambda bl, a: (bl and a.result == 'OK' and has_to_be_ok) or ((bl or a.result != "OK") and not has_to_be_ok),
            result, has_to_be_ok), result)

    results = ''
    problems = ''
    n_dossiers  = len(tst.TESTS)
    n_tests = 0

    for folder_name, group_to_exec in tst.TESTS.items():
        
        # Execution des scenarios
        fake_stud = os.path.join(test_folder, folder_name)
        rs = []
        if(type(group_to_exec) == bool):
            for sc in conf.SCENARIOS_TESTS:
                r, full_res = exec_scenar(fake_stud, sc, group_to_exec)
                rs.append((r, group_to_exec, sc.getName(), full_res))
                n_tests += 1
        elif(type(group_to_exec) == dict):
            for scenario_name, has_to_be_ok in group_to_exec.items():
                r, full_res = exec_scenar(fake_stud, scs[scenario_name], has_to_be_ok)
                rs.append((r, has_to_be_ok, scenario_name, full_res))
                n_tests += 1
        else:
            raise WrongTestConfigurationException("Un dossier de test doit être associé a un booléen " + 
                "indiquant le résultat de tous les scénarios disponibles, ou à un dictionnaire qui à un " +
                "scénario associe son résultat")
        
        # Gestion du retour de la commande

        for elt in rs:
            results += "." if elt[0] else "F"

        if(not functools.reduce(lambda bl, a: a[0] and bl, rs, True)):
            problems += "\n\n\n" + folder_name + "\n"
            problems += "================================\n"
            list_problems = filter(lambda x: not x[0], rs)
            for p in list_problems:
                problems += "Scenario : " + p[2] + "\n"
                problems += "---------------------------------\n"
                if(p[1]):
                    problems += "ECHEC : Le scénario a détecté un problème.\n\n"
                else:
                    problems += "ECHEC : Le scénario s'est exécuté sans détecter de problèmes.\n\n"
                for rst in p[3]:
                    problems += rst.get_message() + "\n"
    

    print("EXECUTION DES TESTS SUR [" + str(n_dossiers) + "] DOSSIERS DE TESTS")
    print("(Nombre de tests exécutés : " + str(n_tests) + ")")
    print("")
    print("Résultat : " + results)
    
    if(results.count("F") == 0):
        print("------------------------------------")
        print("\nOK ! (" + str(results.count(".")) + " tests)")
    else:
        print("\n\n")
        print("====================================")
        print("=      Explication des echecs      =")
        print("====================================")
        print(problems)
        print("\n------------------------------------\n")
        print("\nEchecs : " + str(results.count("F")) + " | Succès : " + str(results.count(".")))