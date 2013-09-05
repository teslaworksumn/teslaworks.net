import json
import os

class ProjectsController:

    def __init__(self, projects_dir):
        self.projects_dir = projects_dir
        self.current_projects = {}
        self.past_projects = {}
        self.all_projects = {}
    
    def get_current_projects(self):
        if not self.current_projects:
            self.load_projects()
        
        return self.current_projects
    
    def get_past_projects(self):
        if not self.past_projects:
            self.load_projects()
        
        return self.past_projects
    
    def get_all_projects(self):
        if not self.all_projects:
            self.load_projects()
        
        return self.all_projects
    
    def load_projects(self):
    
        all_files = os.listdir(self.projects_dir)
        json_files = [f for f in all_files if f.endswith('.json')]
        for file_name in json_files:
            full_file_name = os.path.join(self.projects_dir, file_name)
            with open(full_file_name, 'r') as f:
                data = json.load(f)
        
            project_key = os.path.splitext(file_name)[0]
            
            if 'conclusion_post' in data:
                # This is a past project
                self.past_projects[project_key] = data
            else:
                self.current_projects[project_key] = data
        
        self.all_projects.update(self.current_projects)
        self.all_projects.update(self.past_projects)
    
    def write_projects(self):
        for project_key in self.projects:
            data = self.projects[project_key]
        
            full_file_name = os.path.join(self.projects_dir, project_key + '.json')
            with open(full_file_name, 'w') as f:
                json.dump(data, f)
    
    def set_projects(self, projects):
        self.projects = projects
        self.write_projects()
