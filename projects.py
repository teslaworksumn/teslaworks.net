import json
import os

PROJECT_JSON_LOC = 'data/projects'

def get_projects():
    projects = {}
    
    for file_name in os.listdir(PROJECT_JSON_LOC):
        long_file_name = os.path.join(PROJECT_JSON_LOC, file_name)
        with open(long_file_name, 'r') as file:
            data = json.load(file)
        
        base_file_name = os.path.splitext(file_name)[0]
        projects[base_file_name] = data
    
    return projects
    
    
class ProjectsController:

    def __init__(projects_dir):
        self.projects_dir = projects_dir
    
    def get_projects():
    
        if not projects:
            self.projects = []
            
            for file_name in os.listdir(self.projects_dir):
                full_file_name = os.path.join(self.projects_dir, file_name)
                with open(full_file_name, 'r') as f:
                    data = json.load(f)
                
                id = os.path.splitext(file_name)[0]
                title = data['project_title']
                goal = data['project_goal']
                project = Project(id, title, goal)
                project.details = data['project_details']
                project.needs = data['project_needs']
                
                project.leaders = []
                leaders = data['project_leaders']
                for leader_data in leaders:
                    leader = ProjectLeader(leader_data['name'])
                    leader.email = leader_data['email']
                    leader.phone = leader_data['phone']
                    project.leaders.append(leader)
                
                project.main_image = data['photos']['front_page']
                project.detail_images = data['photos']['detail']
                
                self.projects.append(project)
    
        return self.projects


class Person:

    def __init__(name):
        self.name = name
        
class ProjectLeader(Person):
    pass


class Project:

    def __init__(id, title, goal):
        self.id = id
        self.title = title
        self.goal = goal
