import os
import unittest
import subprocess as sp 
import re
from pathlib import Path

DEPOT = "depot"
TPS = "prof_files"

class AllumettesTest(unittest.TestCase):

    def setUp(self):
        sp.run(["mkdir", "-p", TPS])
        sp.run(["mkdir", "-p", DEPOT])

    def checkStartup(self, path):
        conf = Path(path + "/config.py")
        sources = Path(path + "/public/sources")
        scripts = Path(path + "/scriptsTests")
        
        if(not (scripts.is_dir() and sources.is_dir() and conf.is_file())):
            raise AssertionError("L'un des dossiers de démarrage est manquant")

    def testTruc(self):
        TP = TPS + "/TP_Allumettes"
        # Création d'un TP avec startup
        sp.run(["featpp", "startup", TP])
        # Tester l'existence des fichiers
        self.checkStartup(TP)
        # Déplace les sources vers sources
        sp.run(["rm", "-r", TP + "/public"])
        sp.run(["cp", "-f", "-r", "resources/public", TP ])

        # Modifie fichier config
        sp.run(["cp", "-f", "-r", "resources/config.py", TP + "/config.py"])
        # Scripts de tests dans scripttest
        sp.run(["cp", "-f", "-r", "resources/scripttests", TP + "/scriptsTests"])

        # Génère la bdd avec setup
        sp.run(["featpp", "setup", TP, "resources/liste_etu.csv"])

        # Récupération des fichiers par l'élève
        sp.run(["mkdir", "-p", DEPOT + "/Jojo/TP1"])
        sp.run(["cp", "-r", TP + "/public/*", DEPOT + "/Jojo/TP1/"])

        # L'élève avance dans le TP
        # TODO

        modalites = DEPOT + "/Jojo/TP1/modalites.txt"

        # L'élève veut tester scénario1 uniquement
        self.activer_scenarios(modalites, scenarios_names=["scenario1"])
        sp.run(["featpp", "cycle", DEPOT + "/Jojo/TP1", TP])
        self.assertModalityIsReset(modalites)

        # L'élève veut tester scénario2 uniquement
        self.activer_scenarios(modalites, scenarios_names=["scenario2"])
        sp.run(["featpp", "cycle", DEPOT + "/Jojo/TP1", TP])
        self.assertModalityIsReset(modalites)

        # L'élève veut tester tous les scénarios
        self.activer_scenarios(modalites, all_scs=True)
        sp.run(["featpp", "cycle", DEPOT + "/Jojo/TP1", TP])
        self.assertModalityIsReset(modalites)

        # ... tous les scénarios sans limites
        self.activer_scenarios(modalites, all_not_limited=True)
        sp.run(["featpp", "cycle", DEPOT + "/Jojo/TP1", TP])
        self.assertModalityIsReset(modalites)

        pass

    def assertModalityIsReset(self, file):

        mod_file = open(file, "r")
        content = mod_file.read()
        mod_file.close()

        res = re.search("\?|: oui", content)
        if(res != None):
            raise AssertionError("Le fichier de modalité n'a pas été correctement réinitialisé.")

    def activer_scenarios(self, file, scenarios_names = [], all_scs = False, all_not_limited = False, perturbation = ""):
        
        mod_file = open(file, "r")
        content = mod_file.read()
        mod_file.close()

        for name in scenarios_names:
            re.sub(name + " : non", name + " : oui" + perturbation, content)
        
        if(all_scs):
            re.sub("Voulez-vous jouer tous les tests ? non", "Voulez-vous jouer tous les tests ? oui" + perturbation, content)
        if(all_not_limited):
            re.sub( "Voulez-vous jouer tous les tests qui n'ont pas de restriction de tentatives (infini) ? non" + perturbation, 
                    "Voulez-vous jouer tous les tests qui n'ont pas de restriction de tentatives (infini) ? oui" + perturbation, content)

        mod_file = open(file, "w")
        mod_file.write(content)
        mod_file.close()

    def tearDown(self):
        #sp.run(["rm", "-r", TPS])
        #sp.run(["rm", "-r", DEPOT])
        pass



if __name__ == '__main__':
    unittest.main(verbosity=2)