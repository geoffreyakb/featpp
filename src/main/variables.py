# Modules Python
import json
import os

featpp_path = os.path.dirname(__file__).strip(os.path.join("src", "main"))

with open(os.path.join("settings.json"), 'r') as f:
        paths = json.load(f)

repository_path = paths["repository_path"]
projects_path = paths["projects_path"]