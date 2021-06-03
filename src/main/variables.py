# Modules Python
import json
import os

featpp_path = os.path.dirname(__file__)
featpp_path = os.path.split(featpp_path)[0]

with open(os.path.join(featpp_path, "variables.json"), 'r') as f:
        paths = json.load(f)

repository_path = paths["repository_path"]
projects_path = paths["projects_path"]