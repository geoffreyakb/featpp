from Tool import Tool
from BlackboxResult import BlackboxResult
from typeAnnotations import *
from project_env import ProjectEnv
from isolate import *
import subprocess as sp
import os
import pathlib


class Blackbox():
    
    """
    Classe des tests en boîte noire, compare le résultat d'une exécution d'un programme avec un résultat attendu.
    """

    def __init__(self):
        
        Tool.__init__(self,'')
        
    @argumentType("project_env", ProjectEnv)
    @argumentType("name_file", str)
    def run(self, project_env, name_file):
        
        """
        Paramètres :
            project_env : ProjectEnv - correspond à l'environnement de travail
            command : Str - nom de la commande pour appeler l'outil
        """

        if project_env.is_isolated :
            run_dir = ""
            sources_eleves = ""
        else :
            run_dir =  project_env.project_folder + "/scriptsTests/"
            sources_eleves = project_env.student_project_folder + "/" + project_env.sources_path

            save_point = pathlib.Path().absolute() # Sauvegarde du point actuel

            os.chdir(sources_eleves)

        entries = run_dir + name_file + ".run"
        results = project_env.student_project_folder + "/" + project_env.sources_path + name_file + ".computed"
        expected = project_env.project_folder + "/scriptsTests/" + name_file + ".expected"

        if project_env.is_isolated :
            cp = isolate_run(project_env.isolate_id, "-p", ["/usr/bin/sh", entries])
            
        else :
            cp = sp.run(["sh", entries], stdout=sp.PIPE,timeout=5, text= True)
            os.chdir(save_point)
            

        file = open(results,"w")
        
        file.write(cp.stdout)
        file.close()
        
        diffs = sp.run(["diff","-B",results,expected],stdout = sp.PIPE).stdout.decode("utf-8")
        check_success = (diffs == "")

        

        return BlackboxResult(name_file, check_success, diffs)
