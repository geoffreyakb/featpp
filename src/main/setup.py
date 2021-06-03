# Modules Python
import os
import subprocess
import shutil

# Fichier stockant les paths utiles
from variables import *

def make_path(path):
        if not os.path.exists(path):
            os.mkdir(path)
            return False

def setup(json_file=os.path.join(featpp_path, "settings.json")):    

    if json_file != os.path.join(featpp_path, "settings.json"):
        shutil.copy(json_file, os.path.join(featpp_path, "settings.json"))

    make_path(projects_path)
    for _, path in repository_path.items():
        existed = make_path(path)
        if existed == False:
            with open(f'{path}students.csv', 'w') as file:
                file.write('Students')
            svnAdd = 'svn add ' + path
            subprocess.run(svnAdd, shell=True)
            svnCommit = 'svn commit -m "Une nouvelle promo a été ajoutée." ' + path
            subprocess.run(svnCommit, shell=True)