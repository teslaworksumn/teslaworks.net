import json
import os

class ProjectsController:

    def __init__(self, projects_dir):
        self.projects_dir = projects_dir
        self.projects = {}
    
    def get_projects(self):
    
        if not self.projects:
            all_files = os.listdir(self.projects_dir)
            json_files = [f for f in all_files if f.endswith('.json')]
            for file_name in json_files:
                full_file_name = os.path.join(self.projects_dir, file_name)
                with open(full_file_name, 'r') as f:
                    data = json.load(f)
            
                project_key = os.path.splitext(file_name)[0]
                self.projects[project_key] = data
    
        return self.projects
    
    def write_projects(self):
        for project_key in self.projects:
            data = self.projects[project_key]
        
            full_file_name = os.path.join(self.projects_dir, project_key + '.json')
            with open(full_file_name, 'w') as f:
                json.dump(data, f)
    
    def set_projects(self, projects):
        self.projects = projects
        self.write_projects()
