import unittest
import sys
from _csv import reader

sys.path.append(sys.path[0] + "/../../../")

import env
import test_files.config as config
import os
import time
from shutil import copyfile
from main_setup import setup
from main_cycle import cycle
from ProjectEnv import ProjectEnv

class CycleTest(unittest.TestCase):
    
    def setUp(self):
        self.stu_proj_path = env.PATH + '/tests/unitaires/main/test_files/pveyet/TP'
        self.stu_proj_path2 = env.PATH + '/tests/unitaires/main/test_files/pveyet/TP2'
        self.proj_path = env.PATH + '/tests/unitaires/main/test_files'
        self.csv_path = env.PATH + '/tests/unitaires/main/test_files/students.csv'
        self.project_env = ProjectEnv(self.stu_proj_path, self.proj_path)
        self.project_env2 = ProjectEnv(self.stu_proj_path2, self.proj_path) 
        copyfile(self.proj_path + '/modalities_utility_all_yes2.txt', self.stu_proj_path + '/modalites.txt')
        copyfile(self.proj_path + '/modalities_utility_name_compromised.txt', self.stu_proj_path2 + '/modalites.txt')
        self.restrictions_address = env.PATH + '/tests/unitaires/main/test_files/pveyet/TP/retours/erreurs_contraintes.txt'
        self.synthesis_address = env.PATH + '/tests/unitaires/main/test_files/pveyet/TP/retours/synthese.txt'
        self.details_address = env.PATH + '/tests/unitaires/main/test_files/pveyet/TP/retours/details.txt'
        self.synthesis_address2 = env.PATH + '/tests/unitaires/main/test_files/pveyet/TP2/retours/synthese.txt'
        self.details_address2 = env.PATH + '/tests/unitaires/main/test_files/pveyet/TP2/retours/details.txt'
        
    def test_cycle_error_type_argument(self):
        # -- Test qui vérifie s'il y a une erreur de type dans les arguments de setup
        self.assertRaises(TypeError, cycle, 1)
        
    def test_cycle_restrictions_errors(self):
        # -- Test qui vérifie si le fichier indiquant les scénarios qu'un élève n'a pas pu jouer
        setup(self.proj_path, self.csv_path)
        cycle(self.project_env)
        line2 = "Nombre de tentatives maximum atteint. Il vous est impossible de jouer le scenario : scenario_zero_tentative.\n"
        line1 = "Delai d'attente non respecte. Il vous est impossible de jouer le scenario : scenario_delai_enorme.\n"
        text_to_compare = line1 + line2
        
        reader = open(self.restrictions_address, 'r')
        text = reader.read()
        reader.close()
        self.maxDiff = None
        self.assertEqual(text, text_to_compare)
        
    def test_cycle_created_files(self):
        # -- Test qui vérifie si on crée les fichiers au bon endroit
        setup(self.proj_path, self.csv_path)
        cycle(self.project_env)
        self.assertTrue(os.path.exists(self.restrictions_address))
        self.assertTrue(os.path.exists(self.synthesis_address))
        self.assertTrue(os.path.exists(self.details_address))
        
    def test_cycle_compromised_file(self):
        # -- Test qui vérifie qu'on recrée bien un fichier modalites.txt quand ce dernier est compromis
        setup(self.proj_path, self.csv_path)
        cycle(self.project_env2)
        reader_syn = open(self.synthesis_address2, 'r')
        text_syn = reader_syn.read()
        reader_syn.close()
        reader_det = open(self.details_address2, 'r')
        text_det = reader_det.read()
        reader_det.close()
        self.assertEqual(text_syn, "Fichier modalites compromis - veillez a ne pas modifier autre chose que le terme \'non\' dans ce fichier.\nFichier reinitialise.")
        self.assertEqual(text_det, "Fichier modalites compromis - veillez a ne pas modifier autre chose que le terme \'non\' dans ce fichier.\nFichier reinitialise.")


if __name__ == '__main__':
    unittest.main(verbosity=2)