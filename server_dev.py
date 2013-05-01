import projects
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    project_list = projects.get_projects()
    return render_template('index.html', projects=project_list)

if __name__ == '__main__':
    app.run(debug=True)