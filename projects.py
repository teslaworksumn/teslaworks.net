import json
import os

PROJECT_JSON_LOC = 'data/projects'

def get_projects():
    projects = {}
    
    for file_name in os.listdir(PROJECT_JSON_LOC):
        long_file_name = os.path.join(PROJECT_JSON_LOC, file_name)
        with open(long_file_name, 'r') as file:
            data = json.load(file)
        projects[file_name] = data
    
    return projects
