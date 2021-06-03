import sys

sys.path.append(sys.path[0] + "/../../../../")

import env
from Scenario import Scenario
from ToolResult import *
from Penalty import Penalty

# Cet élément n'apparait jamais dans un fichier de configuration habituel, il n'est là que pour les tests
results = {}

def scenario_test(project_env):
    result = ToolResult("Test", "gn")
    results["scenario_test"] = [result, Penalty("Penalite de 1 point", 1)]
    return results["scenario_test"]

def scenario_test2(project_env):
    result = ToolResult("Test2", "gngn")
    results["scenario_test2"] = [result, Penalty("Penalite de 2 points", 2)]
    return results["scenario_test2"]

def scenario_delai_enorme(project_env):
    result = ToolResult("Test avec gros delai", "OVER 9000")
    results["scenario_delai_enorme"] = [result, Penalty("Penalite de 1 point", 1)]
    return results["scenario_delai_enorme"]

def scenario_cinq_tentatives(project_env):
    result = ToolResult("Test avec cinq tentatives", "5")
    results["scenario_cinq_tentatives"] = [result, Penalty("Penalite de 3 points", 3)]
    return results["scenario_cinq_tentatives"]

def scenario_zero_tentative(project_env):
    result = ToolResult("Test avec zero tentative", "c po zuste")
    results["scenario_zero_tentative"] = [result, Penalty("Penalite de 1 point", 1)]
    return results["scenario_zero_tentative"]

def scenario_en_trop():
    return [ToolResult("Test en trop", "blbl")]

def scenario_invisible():
    result = ToolResult("Test invisible", "bouh")
    results["scenario_invisible"] =  [result]
    return [result]

scenario = Scenario(scenario_test, _delay=0)
scenario2 = Scenario(scenario_test2, _delay=0)
scenario_big_delay = Scenario(scenario_delai_enorme, _delay = 24*3600*100)
scenario_five_attempts = Scenario(scenario_cinq_tentatives, _delay=0, _nb_attempts = 5)
scenario_zero_attempt = Scenario(scenario_zero_tentative, _delay=0, _nb_attempts = 0)

SCENARIOS = [
    scenario,
    scenario2,
    scenario_big_delay,
    scenario_five_attempts,
    scenario_zero_attempt,
    Scenario(scenario_invisible, _visible=False)
]