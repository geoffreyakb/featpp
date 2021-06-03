# Modules Python
import os
import shutil
import traceback
import datetime

# Fichier stockant les paths utiles
from variables import *

def start(project_name):

    # Vérifier qu'un projet portant ce nom n'existe pas déjà
    def existing_path(name):
        path = projects_path + name
        if os.path.exists(path) == True:
            date = datetime.datetime.now()
            # Exemple : tp01_06-05-2021_16:14:26
            name += '_' + date.strftime("%Y-%m-%d_%Hh%Mm%Ss")
            existing_path(name)
        return path

    project_path = existing_path(project_name)

    try:
        shutil.copytree(featpp_path + os.path.join("main", "ressource", "project_sample"), project_path)
    except:
        traceback.print_exc()
        print("\nOperation aborted.")