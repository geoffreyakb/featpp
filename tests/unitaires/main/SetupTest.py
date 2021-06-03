import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
import sqlite3
import os
import functools
from shutil import copyfile
from main_setup import setup
from ProjectEnv import ProjectEnv

class SetupTest(unittest.TestCase):
    
    def setUp(self):
        self.project_folder = env.PATH + '/tests/unitaires/main/test_files'
        self.project_folder_wrong_address = env.PATH + '/tests/unitaires/main/folder_not_found'
        self.csv_path = env.PATH + '/tests/unitaires/main/test_files/students.csv'
        self.csv_path_compromised = env.PATH + '/tests/unitaires/main/test_files/students2.csv'
        self.csv_path_wrong_address = env.PATH + '/tests/unitaires/main/test_files/file_not_found.csv'
        self.database_address = env.PATH + '/tests/unitaires/main/test_files/database_test.db'
        self.scenarios_names = ['scenario_test', 'scenario_test2', 'scenario_delai_enorme', 'scenario_cinq_tentatives', 'scenario_zero_tentative', 'scenario_invisible']
        self.mod_compared = env.PATH + '/tests/unitaires/main/test_files/modalities_utility_all_no.txt'
        self.modalities_address = env.PATH + '/tests/unitaires/main/test_files/public/modalites.txt'
        
    def test_setup_error_type_argument(self):
        # -- Test qui vérifie s'il y a une erreur de type dans les arguments de setup
        self.assertRaises(TypeError, setup, 1, "String")
        self.assertRaises(TypeError, setup, "String", 2)
        
    def test_setup_bdd_students(self):
        # -- Test qui vérifie que tous les étudiants sont bien présents dans la bdd
        setup(self.project_folder, self.csv_path)
        con = sqlite3.connect(self.database_address)
        cur = con.cursor()
        cur.execute("SELECT Students FROM scenario_test")
        execution = cur.fetchall()
        students = [execution[i][0] for i in range(len(execution))]
        self.assertEqual(students, ['pveyet', 'ftroncho', 'ybenabbi', 'tvernize', 'mdehais'])
        con.close()
        
    def test_setup_bdd_scenarios_tables(self):
        # -- Test qui vérifie que toutes les tables sont bien initialisées dans la bdd
        setup(self.project_folder, self.csv_path)
        con = sqlite3.connect(self.database_address)
        cur = con.cursor()
        
        cur.execute("SELECT * FROM scenario_test WHERE Students = '%s'" % 'pveyet')
        execution = cur.fetchone()
        scenario_test = execution[0:2] + execution[3:6]
        self.assertEqual(scenario_test, ('pveyet', '-1', '0', '0', '0'))
        
        cur.execute("SELECT * FROM scenario_test2 WHERE Students = '%s'" % 'pveyet')
        execution = cur.fetchone()
        scenario_test2 = execution[0:2] + execution[3:6]
        self.assertEqual(scenario_test2, ('pveyet', '-1', '0', '0', '0'))
        
        cur.execute("SELECT * FROM scenario_delai_enorme WHERE Students = '%s'" % 'pveyet')
        execution = cur.fetchone()
        scenario_delai_enorme = execution[0:2] + execution[3:6]
        self.assertEqual(scenario_delai_enorme, ('pveyet', '-1', '0', '0', '0'))
        
        cur.execute("SELECT * FROM scenario_cinq_tentatives WHERE Students = '%s'" % 'pveyet')
        execution = cur.fetchone()
        scenario_cinq_tentatives = execution[0:2] + execution[3:6]
        self.assertEqual(scenario_cinq_tentatives, ('pveyet', '5', '0', '0', '0'))
        
        cur.execute("SELECT * FROM scenario_zero_tentative WHERE Students = '%s'" % 'pveyet')
        execution = cur.fetchone()
        scenario_zero_tentative = execution[0:2] + execution[3:6]
        self.assertEqual(scenario_zero_tentative, ('pveyet', '0', '0', '0', '0'))
        
        cur.execute("SELECT * FROM scenario_invisible WHERE Students = '%s'" % 'pveyet')
        execution = cur.fetchone()
        scenario_invisible = execution[0:2] + execution[3:6]
        self.assertEqual(scenario_invisible, ('pveyet', '-1', '0', '0', '0'))
        
        con.close()
        
    def test_setup_modalities_ok(self):
        # -- Test qui vérifie si on a bien créé le bon fichier modalites.txt
        setup(self.project_folder, self.csv_path)
        reader = open(self.mod_compared, 'r')
        text_to_compare = remove_dates(reader.read())
        reader.close()
        
        reader = open(self.modalities_address, 'r')
        text = remove_dates(reader.read())
        reader.close()
        
        self.assertEqual(text, text_to_compare)
            
    def test_setup_students_list_not_found(self):
        # Cas où la liste des étudiants n'est pas renseigné au bon endroit
        with self.assertRaises(SystemExit) as cm:
            setup(self.project_folder, self.csv_path_wrong_address)
        exception = cm.exception
        self.assertEqual(exception.code, 3)
        
    def test_setup_bad_students_list(self):
        # Cas où la liste des étudiants est mal écrite
        with self.assertRaises(SystemExit) as cm:
            setup(self.project_folder, self.csv_path_compromised)
        exception = cm.exception
        self.assertEqual(exception.code, 5)
    
    def test_setup_folder_not_found(self):
        with self.assertRaises(SystemExit) as cm:
            setup(self.project_folder_wrong_address, self.csv_path)
        exception = cm.exception
        self.assertEqual(exception.code, 6)
        
    def test_setup_error_tool_does_not_exist(self):
        # -- Test qui vérifie qu'on lève une exception quand un outil n'existe pas
        pass
    
    def test_setup_error_tool_is_not_there(self):
        # -- Test qui vérifie qu'on lève une exception quand un outil est mal référencé
        pass
    
    def test_setup_error_selfchecks(self):
        # -- Test qui vérifie qu'on lève une exception quand un outil rate son autotest
        pass

def remove_dates(text):
    pieces = text.split('\n')
    for i in range(3, len(pieces)):
        if ((i-3) % 5 == 2 or (i-3) % 5 == 3):
            pieces[i] = pieces[i].split('=')[0]
    return functools.reduce(lambda a,b : a+b+'\n', [""] + pieces)

if __name__ == '__main__':
    unittest.main(verbosity=2)