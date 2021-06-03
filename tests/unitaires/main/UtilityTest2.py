import unittest
import sys

sys.path.append(sys.path[0] + "/../../../")

import env
import test_files2.config as config
import sqlite3
import functools
import utility
from main_setup import create_database

class UtilityTest(unittest.TestCase):
    
    def setUp(self):
        self.path = env.PATH  + '/tests/unitaires/main/test_files2/'
        self.database_address =  self.path + 'database_test.db'
        self.students_list = ["pveyet", "ftroncho", "ybenabbi", "tvernize", "mdehais"]
        self.scenarios = config.SCENARIOS
        create_database(self.database_address, self.scenarios, self.students_list)
        self.exec("UPDATE scenario_cinq_tentatives SET Attempts = '5' WHERE Students = 'pveyet'")
        progress_address = self.path + 'avancee_globale_test2.txt'

        reader = open(progress_address, 'r')
        self.progress_text = reader.read()
        reader.close()
        
    def test_print_overall_progress_no_marks_and_penalties(self):
        text = utility.print_overall_progress(self.database_address, self.students_list, self.scenarios)
        self.maxDiff = None
        self.assertEqual(remove_date(text), remove_date(self.progress_text))

    def exec(self, request):
        con = sqlite3.connect(self.database_address)
        cur = con.cursor()
        cur.execute(request)
        con.commit()
        con.close()
        
def remove_date(text):
    pieces = text.split('\n')
    pieces[0] = pieces[0].split(' : ')[0]
    return functools.reduce(lambda a,b : a+b+'\n', [""] + pieces)
    

if __name__ == '__main__':
    unittest.main(verbosity=2)