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
    results.append(Text("My Scenario"))
    return results

def scenario2(project_env):
    results = []
    results.append(Text("My Scenario 2"))
    return results

def scenario_test(project_env):
    results = []
    results.append(javaCompiler.run(project_env, ["HelloWorld.java"]))
    results.append(blackBox.run(project_env, "helloWorld"))
    return results

def bad_scenario_test(project_env):
    results = []
    results.append(javaCompiler.run(project_env, ["HelloWorld.java"]))
    results.append(blackBox.run(project_env, "BadHelloWorld"))
    return results


# ---------------------------------------------
# Liste des scénarios
# ---------------------------------------------

SCENARIOS = [
    Scenario(scenario1),
    Scenario(scenario2)
]

SCENARIOS_TESTS = SCENARIOS + [
    Scenario(scenario_test),
    Scenario(bad_scenario_test),
]