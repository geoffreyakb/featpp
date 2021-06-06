# Modules Python
import sys
import re

# Fichier stockant les paths utiles
from variables import *

# Module FEAT++ utile pour parcourir le dossier src et importer les autres modules
sys.path.append(featpp_path)
import env

# Sous-programmes principaux
from setup import setup
from start import start
from runtests import runtests
from send import send
from evaluate import evaluate
from progress import progress

# --------------------------------------------------------------------

# Definitions
def help(sub=None):

    help_file = os.path.join(featpp_path, "main", "resource", "help", "help.txt")

    with open(help_file, "r") as file:
        if sub:
            text = file.read()
            parsed = re.search("\|" + sub + "(.*?)\n\n", text, re.S)
            if parsed:
                print(parsed.group(0))
                return None

        print(file.read())

    file.close()
    sys.exit(1)

# Cas où aucun argument n'est appelé ou si l'utilisateur veut de l'aide
if (len(sys.argv) == 1) or (sys.argv[1] == "help"):
    help()

subprogs = {
    "setup" : [setup, 0],
    "start" : [start, 1],
    "runtests" : [runtests, 1],
    "send" : [send, len(sys.argv)-2],
    "evaluate": [evaluate, len(sys.argv)-2],
    "progress" : [progress, 2]
}

subprog = subprogs.get(sys.argv[1], [help, 0])
nb_args = subprog[1]

# Cas où trop peu d'arguments sont appelés
if (nb_args+2 > len(sys.argv)) and (subprog != "setup"):
    help(sys.argv[1])
else:
    arg_list = sys.argv[2:nb_args+2]
    if arg_list:
        arg_list[-1] = arg_list[-1].strip()         # Enlève un '\r' problématique sur MacOS
subprog[0](*arg_list)