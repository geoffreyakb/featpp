# Modules Python
import json
import os

featpp_path = os.path.dirname(__file__)

with open(os.path.join("variables.json"), 'r') as f:
        paths = json.load(f)

repository_path = paths["repository_path"]
projects_path = paths["projects_path"]