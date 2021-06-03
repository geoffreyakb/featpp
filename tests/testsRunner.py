import sys

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append(sys.path[0]+'/../')

from env import *
import unittest

add_path_directories(PATH+"/tests/unitaires")


def importAllTests(path):
    list_imports = {}
    l = glob.glob(path+'/*') 
    for i in l: 
        if os.path.isdir(i) and i[-11:]!="__pycache__" and i[-3:]!= "out"  :
            list_imports.update(importAllTests(i))
        elif i[-7:]=="Test.py":
            toImport = i.split("/")[-1][:-3]
            print(toImport)
            list_imports[toImport] = getattr(__import__(toImport), toImport)
        
    return list_imports


list_imp = importAllTests(PATH+"/tests/unitaires")

globals().update(list_imp)

if __name__ == '__main__':
    unittest.main()