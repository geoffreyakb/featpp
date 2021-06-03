import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
import sqlite3
import os
import functools
import datetime
import re
from shutil import copyfile
from main_progress import progress


class ProgressTest(unittest.TestCase):
    
    def setUp(self):
        self.project_folder = env.PATH + '/tests/unitaires/main/test_files'
        self.project_folder_wrong_address = env.PATH + '/tests/unitaires/main/folder_not_found'
        self.csv_path = env.PATH + '/tests/unitaires/main/test_files/students.csv'
        self.csv_path_compromised = env.PATH + '/tests/unitaires/main/test_files/students2.csv'
        self.csv_path_wrong_address = env.PATH + '/tests/unitaires/main/test_files/file_not_found.csv'
        self.database_address = env.PATH + '/tests/unitaires/main/test_files/database_test.db'
        
    def test_progress_ok(self):
        progress(self.project_folder, self.csv_path)
        date = str(datetime.datetime.today().strftime("%Y-%m-%d"))
        # Vérification de l'existence du nouveau fichier (sachant que les tests pour vérifier s'il est bien écrit sont dans UtilityTest)
        fichiers = [f for f in os.listdir(self.project_folder) if f.startswith('avancee_globale_' + date)]
        self.assertTrue(fichiers != [])
        for f in fichiers:
            os.remove(self.project_folder + '/' + f)
        
    def test_progress_error_type_argument(self):
        # -- Test qui vérifie s'il y a une erreur de type dans les arguments de setup
        self.assertRaises(TypeError, progress, 1, "String")
        self.assertRaises(TypeError, progress, "String", 2)
        
    def test_progress_students_list_not_found(self):
        # Cas où la liste des étudiants n'est pas renseigné au bon endroit
        with self.assertRaises(SystemExit) as cm:
            progress(self.project_folder, self.csv_path_wrong_address)
        exception = cm.exception
        self.assertEqual(exception.code, 3)
        
    def test_progress_bad_students_list(self):
        # Cas où la liste des étudiants est mal écrite
        with self.assertRaises(SystemExit) as cm:
            progress(self.project_folder, self.csv_path_compromised)
        exception = cm.exception
        self.assertEqual(exception.code, 4)
    
    def test_progress_folder_not_found(self):
        # Cas où le dossier n'est pas renseigné au bon endroit
        with self.assertRaises(SystemExit) as cm:
            progress(self.project_folder_wrong_address, self.csv_path)
        exception = cm.exception
        self.assertEqual(exception.code, 5)

if __name__ == '__main__':
    unittest.main(verbosity=2)