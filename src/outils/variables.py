# Modules Python
import json
import os

featpp_path = os.path.dirname(__file__).strip("main") + os.sep

with open(featpp_path + "settings.json", 'r') as f:
        paths = json.load(f)

repository_path = paths["repository_path"]
projects_path = paths["projects_path"]