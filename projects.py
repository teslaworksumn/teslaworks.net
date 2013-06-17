import json

PROJECT_JSON_LOC = 'projects.json'

def get_projects():
	with open(PROJECT_JSON_LOC, 'r') as f:
		data = json.load(f)
	project_list = data['projects']
	return project_list