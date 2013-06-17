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
    return "Bet you can't wait to join %s, huh?" % project


if __name__ == '__main__':
    app.run(debug=True)
