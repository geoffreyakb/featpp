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

def Verif_Partie(project_env):
    results = []
    results.append(javaCompiler.run()
    return results

def scenario2(project_env):
    results = []
    results.append(Text("My Scenario 2"))
    return results


# ---------------------------------------------
# Liste des scénarios
# ---------------------------------------------

SCENARIOS = [
    Scenario(Verif_Partie),
    Scenario(scenario2)
]