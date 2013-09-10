from flask import Flask, request, url_for, render_template, flash, redirect, abort
from flask_mail import Mail, Message
from projects_controller import ProjectsController
from redirects_controller import RedirectsController
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.url_map.strict_slashes = False
app.config.update(config.APP_CONFIG)

app.config.update(config.MAIL_SETTINGS)
mail = Mail(app)

projects_controller = ProjectsController(config.DATA_DIR)
redirects_controller = RedirectsController(config.DATA_DIR)


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
    if not request.args:
        fields = {}
        return render_template('start_project.html')

    name = request.args.get('name')
    email = request.args.get('email')
    title = request.args.get('title')
    desc = request.args.get('desc')
    
    fields = {'name': name, 'email': email, 'title': title, 'desc': desc}
    
    if not name or not email or not title or not desc:
        return render_template('start_project.html', fields=fields)
    
    msg = Message("New Project Request")
    msg.add_recipient(config.CONTACT_EMAIL)
    msg.html = render_template('project_request.html', name=name, email=email, title=title, desc=desc)
    
    mail.send(msg)
    
    flash("Success! Your project has been submitted to the officer board, and you'll hear back from us in a few days.", 'success')
    return redirect(url_for('index'))

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
