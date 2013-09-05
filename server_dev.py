from projects_controller import ProjectsController
from flask import Flask, render_template, redirect, abort


PROJECTS_DIR = 'data/projects'

app = Flask(__name__)
projects_controller = ProjectsController(PROJECTS_DIR)

app.url_map.strict_slashes = False


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    projects = projects_controller.get_current_projects()
    return render_template('index.html', projects=projects)

@app.route('/blog')
def blog():
    return "Flasktopress isn't quite ready yet, but we're stoked that it's coming."

@app.route('/start')
def start_project():
    return render_template('start_project.html')

@app.route('/<project>')
def project(project):

    projects = projects_controller.get_all_projects()
    if project in projects:
        project_data = projects[project]
        if 'conclusion_post' in project_data:
            # The project is over, we should redirect to the post
            return redirect(project_data['conclusion_post'])
        else:
          return render_template('project.html', project_data=project_data)

    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
