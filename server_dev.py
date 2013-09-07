from projects_controller import ProjectsController
from redirects_controller import RedirectsController
from flask import Flask, render_template, redirect, abort


DATA_DIR = 'data'

app = Flask(__name__)
app.url_map.strict_slashes = False

projects_controller = ProjectsController(DATA_DIR)
redirects_controller = RedirectsController(DATA_DIR)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    current_projects = projects_controller.get_current_projects()
    past_projects = projects_controller.get_past_projects()
    return render_template('index.html', current_projects=current_projects, past_projects=past_projects)

@app.route('/start')
def start_project():
    return render_template('start_project.html')

@app.route('/<dynamic>')
def project(dynamic):

    projects = projects_controller.get_all_projects()
    redirects = redirects_controller.get_redirects()

    # First, test if if it's a project
    if dynamic in projects:
        project_data = projects[dynamic]
        if 'conclusion_post' in project_data:
            # The project is over, we should redirect to the post
            return redirect(project_data['conclusion_post'])
        else:
          return render_template('project.html', project_data=project_data)

    # Next, check if it's a redirect
    elif dynamic in redirects:
        return redirect(redirects[dynamic])

    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
