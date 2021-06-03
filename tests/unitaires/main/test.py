import sys

sys.path.append(sys.path[0] + "/../../../")

import env
import time
from main_setup import setup
from main_cycle import cycle
from config import SCENARIOS
from utility import print_overall_progress

database = env.PATH + '/tests/unitaires/main/database_test.db'
students = ["pveyet", "ftroncho", "ybenabbi", "tvernize", "mdehais"]

setup(env.PATH + '/tests/unitaires/main/', env.PATH + '/tests/unitaires/main/test_files/students.csv')
time.sleep(6)
cycle(env.PATH + '/tests/unitaires/main/pveyet/TP/', env.PATH + '/tests/unitaires/main/')
time.sleep(3)

print(print_overall_progress(database, students, SCENARIOS))