from Scenario import Scenario
from tools import *
from Text import Text


# ---------------------------------------------
# Outils disponibles
# ---------------------------------------------

javaCompiler = JavaCompiler() 
blackBox = Blackbox()


# ---------------------------------------------
# Definition des scénarios 
# ---------------------------------------------

def scenario1(project_env):
    results = []
    results.append(blackBox.run("3puis4"))
    return results


# ---------------------------------------------
# Liste des scénarios
# ---------------------------------------------

SCENARIOS = [
    Scenario(scenario1)
]

SCENARIOS_TEST = SCENARIOS + [

]