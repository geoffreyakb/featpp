import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
import test_files.config as config
import sqlite3
import os
import functools
import utility
from main_setup import create_database
from ProjectEnv import ProjectEnv
from ToolResult import ToolResult
from Penalty import Penalty
from unittest_data_provider import data_provider
from UtilityDataProviders import *

class UtilityTest(unittest.TestCase):
    
    def setUp(self):
        self.path = env.PATH  + '/tests/unitaires/main/test_files/'

        self.database_address =  self.path + 'database_test.db'
        self.students_list = ["pveyet", "ftroncho", "ybenabbi", "tvernize", "mdehais"]
        self.results = config.results

        # (Re)initialisation de la base de données
        self.scenarios = config.SCENARIOS
        create_database(self.database_address, self.scenarios, self.students_list)
        self.exec("UPDATE scenario_cinq_tentatives SET Attempts = '5' WHERE Students = 'pveyet'")

        # Définitions des fichiers utiles
        self.mod_result = self.path + 'mod_result.txt'
        self.synthesis_address = env.PATH  + '/tests/unitaires/main/test_files/pveyet/TP/retours/synthese.txt'
        self.details_address = env.PATH  + '/tests/unitaires/main/test_files/pveyet/TP/retours/details.txt'
        self.synthesis_print_address = self.path + 'synthese_print.txt'
        self.details_print_address = self.path + 'details_print.txt'
        self.project_env = ProjectEnv(env.PATH + '/tests/unitaires/main/test_files/', env.PATH + '/tests/unitaires/main/test_files/')
        
        modalities_address = self.path + 'public/modalites.txt'
        modalities_address2 = self.path + 'modalites2.txt'
        modalities_address3 = self.path + 'modalites3.txt'
        progress_address = self.path + 'avancee_globale_test.txt'
        synthesis_ok_address = self.path + 'synthese_ok.txt'
        details_ok_address = self.path + 'details_ok.txt'
        
        reader = open(modalities_address, 'r')
        self.modalities_text_ok = reader.read()
        reader.close()
        
        reader2 = open(modalities_address2, 'r')
        self.modalities_text_ok2 = reader2.read()
        reader2.close()
        
        reader3 = open(modalities_address3, 'r')
        self.modalities_text_ok3 = reader3.read()
        reader3.close()
        
        reader4 = open(self.synthesis_print_address, 'r')
        self.synthesis_to_compare = reader4.read()
        reader4.close()
        
        reader5 = open(self.details_print_address, 'r')
        self.details_to_compare = reader5.read()
        reader5.close()
        
        reader6 = open(progress_address, 'r')
        self.progress_text = reader6.read()
        reader6.close()
        
        reader7 = open(synthesis_ok_address, 'r')
        self.syn_ok = reader7.read()
        reader7.close()
        
        reader8 = open(details_ok_address, 'r')
        self.det_ok = reader8.read()
        reader8.close()
    
# ----- TESTS POUR MODALITIES_TEXT -----
    def test_modalities_text_error_type(self):
        self.assertRaises(TypeError, utility.modalities_text, 1, "String", "String")
        self.assertRaises(TypeError, utility.modalities_text, [], 2, "String")
        self.assertRaises(TypeError, utility.modalities_text, [], "String", 3)
        
    def test_modalities_text_init(self):
        # -- Test pour l'initialisation
        generated = remove_dates(utility.modalities_text(self.scenarios, self.database_address))
        needed = remove_dates(self.modalities_text_ok)
        self.assertEqual(generated, needed)
        
    def test_modalities_text_update(self):
        # -- Test pour un update du fichier d'un étudiant
        self.exec("UPDATE scenario_cinq_tentatives SET Attempts = '4' WHERE Students = 'pveyet'")
        generated = remove_dates(utility.modalities_text(self.scenarios, self.database_address, "pveyet"))
        needed =  remove_dates(self.modalities_text_ok2)
        self.maxDiff = None
        self.assertEqual(generated, needed)

# ----- TESTS POUR GET_SCENARIO -----
    def test_get_scenarios_error_type(self):
        self.assertRaises(TypeError, utility.get_scenarios, 1, [])
        self.assertRaises(TypeError, utility.get_scenarios, "String", 2,)

    @data_provider(get_scenarios_ok_provider)
    def test_get_scenarios_ok(self, modality_file, final_list, description = ""):        
        self.assertEqual(utility.get_scenarios(modality_file, self.scenarios), final_list, description)

    @data_provider(get_scenarios_not_ok_provider)
    def test_get_scenarios_not_ok(self, modality_file, description = ""):        
        with self.assertRaises(utility.CompromisedFileException, msg = description):
            utility.get_scenarios(modality_file, self.scenarios)

# ----- TESTS POUR RUN_SCENARIOS -----
    def test_run_scenarios_error_type(self):
        self.assertRaises(TypeError, utility.run_scenarios, 1, "String", "String", "String", [])
        self.assertRaises(TypeError, utility.run_scenarios, [], 2, "String", "String", [])
        self.assertRaises(TypeError, utility.run_scenarios, [], "String", 3, "String", [])
        self.assertRaises(TypeError, utility.run_scenarios, [], "String", "String", 4, [])
        self.assertRaises(TypeError, utility.run_scenarios, [], "String", "String", "String", 5)
        
    def test_run_scenarios_empty(self):
        # -- Test sans scénario
        self.assertEqual(utility.run_scenarios([], self.database_address, self.mod_result, "pveyet", self.project_env, self.scenarios), [])
        
        # Vérification que mod_result est bien réinitialisé
        reader_mod = open(self.mod_result, 'r')
        text_to_compare = remove_dates(functools.reduce(lambda a,b : a+b, reader_mod.readlines()))
        reader_mod.close()
        self.maxDiff = None
        self.assertEqual(text_to_compare, remove_dates(self.modalities_text_ok), "Le fichier modalites.txt recréé n'est pas le bon.")
        
        # Destruction des fichiers créés
        os.remove(self.mod_result)
        
    def test_run_scenarios_all_scenarios(self):
        # -- Test avec tous les scénarios jouables (scenario_test, scenario_test2 et scenario_cinq_tentatives)
        self.assertEqual(utility.run_scenarios([config.scenario, config.scenario2, config.scenario_five_attempts], self.database_address, self.mod_result, "pveyet", self.project_env, self.scenarios), [self.results['scenario_test'], self.results['scenario_test2'], self.results['scenario_cinq_tentatives']])
        
        # Vérification que mod_result est bien réinitialisé avec la bonne valeur pour les tentatives
        reader_mod = open(self.mod_result, 'r')
        text_to_compare = remove_dates(functools.reduce(lambda a,b : a+b, reader_mod.readlines()))
        
        reader_mod.close()
        self.maxDiff = None
        self.assertEqual(text_to_compare, remove_dates(self.modalities_text_ok3), "Le fichier modalites.txt recréé n'est pas le bon.")
        
        # Modification de la bdd pour les autres tests
        con = sqlite3.connect(self.database_address)
        cur = con.cursor()
        cur.execute("UPDATE scenario_cinq_tentatives SET Attempts = '5' WHERE Students = 'pveyet'")
        con.commit()
        con.close()
        
        # Destruction des fichiers créés
        os.remove(self.mod_result)


# ----- TESTS POUR PRINT_RESULTS -----
    def test_print_results_error_type(self):
        self.assertRaises(TypeError, utility.print_results, 1, "String", 0)
        self.assertRaises(TypeError, utility.print_results, [], 2, 0)
        self.assertRaises(TypeError, utility.print_results, [], "String", '3')
    
    def test_print_results_empty(self):
        # -- Test sans résultat
        # Préparatifs
        open(self.synthesis_address, 'w').close()
        open(self.details_address, 'w').close()
        utility.print_results([], self.synthesis_address, 0)
        utility.print_results([], self.details_address, 1)
        
        # Vérification que synthese.txt et details.txt sont vides
        self.assertTrue(os.path.getsize(self.synthesis_address)==0, "Le fichier de synthese devrait etre vide !")
        self.assertTrue(os.path.getsize(self.details_address)==0, "Le fichier de details devrait etre vide !")
        
        # Destruction des fichiers créés
        os.remove(self.details_address)
        os.remove(self.synthesis_address)
    
    def test_print_results_all_results(self):
        # -- Test avec tous les résultats des scénarios jouables
        # Préparatifs
        open(self.synthesis_address, 'w').close()
        open(self.details_address, 'w').close()
        utility.print_results([[utility.ToolResult("Test", "gn")], [utility.ToolResult("Test2", "gngn")], [utility.ToolResult("Test avec cinq tentatives", "5")]], self.synthesis_address, 0)
        utility.print_results([[utility.ToolResult("Test", "gn")], [utility.ToolResult("Test2", "gngn")], [utility.ToolResult("Test avec cinq tentatives", "5")]], self.details_address, 1)
        
        # Vérification que synthese.txt et details. txt contiennent bien ce qu'il faut
        self.assertEqual(os.path.getsize(self.synthesis_address), os.path.getsize(self.synthesis_print_address))
        self.assertEqual(os.path.getsize(self.details_address), os.path.getsize(self.details_print_address))
        
        reader_synthesis = open(self.synthesis_address, 'r')
        text_to_compare = reader_synthesis.read()
        reader_synthesis.close()
        
        reader_details = open(self.synthesis_address, 'r')
        text_to_compare2 = reader_details.read()
        reader_details.close()
        
        self.assertEqual(text_to_compare, self.synthesis_to_compare, "Le fichier synthese.txt n'est pas écrit correctement.")
        self.assertEqual(text_to_compare2, self.details_to_compare, "Le fichier details.txt n'est pas écrit correctement.")

        # Destruction des fichiers créés
        os.remove(self.details_address)
        os.remove(self.synthesis_address)

# ----- TESTS POUR REPORT -----
    def test_report_error_type(self):
        self.assertRaises(TypeError, utility.report, 1, [], "String", "String")
        self.assertRaises(TypeError, utility.report, [], 2, "String", "String")
        self.assertRaises(TypeError, utility.report, [], [], 3, "String")
        self.assertRaises(TypeError, utility.report, [], [], "String", 4)
        
    def test_report_ok(self):
        # -- Test pour vérifier le bon fonctionnement de report
        open(self.synthesis_address, 'w').close()
        open(self.details_address, 'w').close()
        # Préparation de la base de données
        con = sqlite3.connect(self.database_address)
        cur = con.cursor()
        cur.execute("UPDATE scenario_cinq_tentatives SET Attempts_Done = '1' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_cinq_tentatives SET Penalty = '2' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_cinq_tentatives SET Mark = '6' WHERE Students = 'pveyet';")
        con.commit()
        con.close()
        results_list = [[ToolResult("Test", "gn"), Penalty("Penalite de 1 point", 1)], [ToolResult("Test2", "gngn"), Penalty("Penalite de 2 points", 2)], [ToolResult("Test avec cinq tentatives", "5"), Penalty("Penalite de 3 points", 3)]]
        results_list.append(utility.report([config.scenario, config.scenario2, config.scenario_five_attempts], results_list, self.database_address, "pveyet"))
       
        # Création des données
        utility.print_results(results_list, self.synthesis_address, 0)
        utility.print_results(results_list, self.details_address, 1)

        # Comparaison
        reader = open(self.synthesis_address, 'r')
        syn = reader.read()
        reader.close()
        reader = open(self.details_address, 'r')
        det = reader.read()
        reader.close()
        self.assertEqual(syn, self.syn_ok)
        self.assertEqual(det, self.det_ok)
        
        # Destruction des fichiers créés
        os.remove(self.details_address)
        os.remove(self.synthesis_address)
        

# ----- TESTS POUR OVERALL_PROGRESS -----
    def test_print_overall_progress_error_type(self):
        self.assertRaises(TypeError, utility.print_overall_progress, 1, ["String"], [])
        self.assertRaises(TypeError, utility.print_overall_progress, "String", 2, [])
        self.assertRaises(TypeError, utility.print_overall_progress, "String", ["String"], 3)

    def test_print_overall_progress_empty(self):
        self.assertEqual(utility.print_overall_progress(self.database_address, [], self.scenarios), "La liste des etudiants est vide.")
        self.assertEqual(utility.print_overall_progress(self.database_address, self.students_list, []), "La liste des scenarios est vide.")
        
    def test_print_overall_progress_ok(self):
        # Préparation de la base de données
        con = sqlite3.connect(self.database_address)
        cur = con.cursor()
        cur.execute("UPDATE scenario_test SET Attempts_Done = '1' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_test SET Penalty = '1' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_test SET Mark = '0' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_test2 SET Attempts_Done = '2' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_test2 SET Penalty = '2' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_test2 SET Mark = '3' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_cinq_tentatives SET Attempts_Done = '1' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_cinq_tentatives SET Penalty = '3' WHERE Students = 'pveyet';")
        cur.execute("UPDATE scenario_cinq_tentatives SET Mark = '5' WHERE Students = 'pveyet';")
        con.commit()
        con.close()
        
        # Vérification qu'on obtient bien le bon texte en sortie avec les valeurs précédentes
        text = utility.print_overall_progress(self.database_address, self.students_list, self.scenarios)
        self.assertEqual(remove_date(text), remove_date(self.progress_text))
        
    def exec(self, request):
        con = sqlite3.connect(self.database_address)
        cur = con.cursor()
        cur.execute(request)
        con.commit()
        con.close()
        
def remove_dates(text):
    pieces = text.split('\n')
    for i in range(3, len(pieces)):
        if ((i-3) % 5 == 2 or (i-3) % 5 == 3):
            pieces[i] = pieces[i].split('=')[0]
    return functools.reduce(lambda a,b : a+b+'\n', [""] + pieces)

def remove_date(text):
    pieces = text.split('\n')
    pieces[0] = pieces[0].split(' : ')[0]
    return functools.reduce(lambda a,b : a+b+'\n', [""] + pieces)
    

if __name__ == '__main__':
    unittest.main(verbosity=2)