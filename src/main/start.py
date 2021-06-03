# Modules Python
import os
import shutil
import traceback
import datetime

# Fichier stockant les paths utiles
from variables import *

def start(project_name):

    project_path = projects_path + project_name

    try:
        shutil.copytree(os.path.join(featpp_path, "resource", "project_sample"), project_path)
    except FileExistsError:
        date = datetime.datetime.now()
        # Exemple : tp01_06-05-2021_16:14:26
        project_name += '_' + date.strftime("%Y-%m-%d_%Hh%Mm%Ss")
        start(project_name)
    except:
        traceback.print_exc()
        print("\nOperation aborted.")
