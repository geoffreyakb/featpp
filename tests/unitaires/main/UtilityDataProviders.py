import test_files.config as config
import sys
sys.path.append(sys.path[0] + "/../../../")
import env

path = env.PATH + '/tests/unitaires/main/test_files/'

def get_scenarios_ok_provider():
    all_scenarios = [config.scenario, config.scenario2, config.scenario_big_delay, config.scenario_five_attempts, config.scenario_zero_attempt]
    all_infinite = [config.scenario, config.scenario2, config.scenario_big_delay, config.scenario_five_attempts]
    data = (
        (path + 'modalities_utility_all_no.txt', [], "Test sans aucun scénario à jouer"),
        (path + 'modalities_utility_all_yes.txt', all_scenarios, "Test avec tous les scénarios à jouer"),
        (path + 'modalities_utility_all_yes2.txt', all_scenarios, "Test avec tous les scénarios à jouer en utilisant la première clause"),
        (path + 'modalities_utility_some_yes.txt',[config.scenario, config.scenario_big_delay], "Test avec seulement quelques scénarios"),
        (path + 'modalities_utility_all_infinite.txt', all_infinite, "Test avec les scénarios sans restriction de tentatives"),
        (path + 'modalities_utility_one_useless_row_missing.txt', [], "Test avec suppression d'une ligne"),
    )
    return data

def get_scenarios_not_ok_provider():
    data = (
        (path + 'modalities_utility_one_row_missing.txt', "Test avec suppression d'une ligne"),
        (path + 'modalities_utility_one_bloc_missing.txt', "Test avec suppression d'un bloc complet"),
        (path + 'modalities_utility_empty.txt', "Test avec suppression du fichier"),
        (path + 'modalities_utility_name_compromised.txt', "Test avec modification d'un nom de scénario"),
        (path + 'modalities_utility_first_clause_missing.txt', "Test avec suppression de la première ligne"),
        (path + 'modalities_utility_second_clause_missing.txt', "Test avec suppression d'un bloc complet"),
        (path + 'modalities_utility_yes_no_missing.txt', "Test avec suppression d'un oui/non"),
    )
    return data