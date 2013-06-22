import projects
from flask import Flask, render_template, abort
app = Flask(__name__)
app.url_map.strict_slashes = False

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    project_list = projects.get_projects()
    return render_template('index.html', projects=project_list)

@app.route('/blog')
def blog():
    return "Flasktopress isn't quite ready yet, but we're stoked that it's coming."

@app.route('/<project>')
def project(project):
    project_list = projects.get_projects()
    if project in project_list:
        project_data = project_list[project]
        return render_template('project.html', project_data=project_data)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
