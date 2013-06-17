import projects
from flask import Flask, render_template
app = Flask(__name__)


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
        return "Contact %s to join the %s project!" % (project_data['project_leaders'][0]['name'], project_data['project_title'])
    else:
        return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
