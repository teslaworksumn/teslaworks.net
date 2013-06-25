import os
import projects_controller
import server_dev

def page_exists(response):
    return response.status_code == 200

def test_trailing_slash_agnosticism():
    server_dev.app.config['TESTING'] = True
    app = server_dev.app.test_client()
    
    response_no_slashes = app.get('/lightshow')
    assert page_exists(response_no_slashes)
    
    response_with_slashes = app.get('/lightshow/')
    assert page_exists(response_with_slashes)

def test_projects_controller_load():
    pc = projects_controller.ProjectsController('data/projects')
    projects = pc.get_projects()
    
    assert 'lightshow' in projects
    
    assert projects['lightshow']['project_title'] == "CSE Light Show"
    assert 'engineering' in projects['lightshow']['project_needs']

def test_projects_controller_write():
    pc = projects_controller.ProjectsController('data/projects')
    projects = pc.get_projects()
    
    # Store current values
    current_title = projects['lightshow']['project_title']
    current_marketing_list = projects['lightshow']['project_needs']['marketing']
    
    # Change current values
    projects['lightshow']['project_title'] = "CSE Light Show 2013"
    projects['lightshow']['project_needs']['marketing'].append("Donation drummers for the Amplatz Childrens' Hospital")
    
    # Store, obliterate, and reload
    pc.set_projects(projects)
    pc.projects = {}
    projects = pc.get_projects()
    
    # Check changed values
    assert projects['lightshow']['project_title'] == "CSE Light Show 2013"
    assert "Donation drummers for the Amplatz Childrens' Hospital" in projects['lightshow']['project_needs']['marketing']
    
    # Verify other contents are unchanged
    assert 'engineering' in projects['lightshow']['project_needs']
    
    # Put things back
    projects['lightshow']['project_title'] = current_title
    projects['lightshow']['project_needs']['marketing'] = current_marketing_list
    pc.set_projects(projects)


def test_projects_controller_create():
    pc = projects_controller.ProjectsController('data/projects')
    projects = pc.get_projects()
    
    projects['robotkitten'] = { 'project_title': "Fluffy Friendly Robot Kitten", 'project_goal': "Construct the most adorable animatronic friend ~*~EVER~*~" }
    
    pc.set_projects(projects)
    
    assert projects['robotkitten']['project_title'] == "Fluffy Friendly Robot Kitten"
    
    os.remove('data/projects/robotkitten.json')
