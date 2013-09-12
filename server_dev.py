from flask import Flask, request, url_for, render_template, flash, redirect, abort
from jinja2 import evalcontextfilter, Markup, escape
from flask_mail import Mail, Message
from projects_controller import ProjectsController
from redirects_controller import RedirectsController
import config
import re

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.url_map.strict_slashes = False
app.config.update(config.APP_CONFIG)

app.config.update(config.MAIL_SETTINGS)
mail = Mail(app)

projects_controller = ProjectsController(config.DATA_DIR)
redirects_controller = RedirectsController(config.DATA_DIR)

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


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
        return render_template('start.html', q={}, errors={})

    q = request.args
    errors = {}

    if not q['name']:
        errors['name'] = "We need to know who you are!"

    if not q['email']:
        errors['email'] = "We need to know how to get ahold of you!"

    if not q['ptitle']:
        errors['ptitle'] = "We need to know what to call your project!"
    
    if not q['desc']:
        errors['desc'] = "We need to know what your project is about!"

    if not errors:
        msg = Message("New Project Request")
        msg.add_recipient(config.CONTACT_EMAIL)
        msg.html = render_template('mail/start.html', q=q)
        
        mail.send(msg)

        flash("Success! Your project has been submitted to the officer board, and you'll hear back from us in a few days.", 'success')
        return redirect(url_for('index'))

    return render_template('start.html', q=q, errors=errors)

@app.route('/<dynamic>')
def dynamic(dynamic):

    projects = projects_controller.get_all_projects()
    redirects = redirects_controller.get_redirects()

    # First, test if if it's a project
    if dynamic in projects:
        project_data = projects[dynamic]
        if 'conclusion_post' in project_data:
            # The project is over, we should redirect to the post
            return redirect(project_data['conclusion_post'])
        else:
          return render_project(dynamic, project_data)

    # Next, check if it's a redirect
    elif dynamic in redirects:
        return redirect(redirects[dynamic])

    else:
        abort(404)

def render_project(project_name, project_data):
    if not request.args:
        return render_template('project.html', project_data=project_data)

    fields = {}

    join_email = request.args.get('join[email]')
    ask_email = request.args.get('ask[email]')
    ask_msg = request.args.get('ask[msg]')

    if join_email:
        fields['join'] = {'email': join_email}

        msg = Message("Someone wants to join your project!")
        msg.add_recipient(project_data['project_leaders'][0]['email'])
        msg.html = render_template('mail/join_project.html', email=join_email)

        mail.send(msg)

        flash_msg = "Success! You have successfully asked to join the " + project_data['project_title'] + " project!"
        flash(flash_msg, 'success')
        redirect_path = "/" + project_name
        return redirect(redirect_path)

    if ask_email or ask_msg:
        fields['ask'] = {'email': ask_email, 'msg': ask_msg}
    
    if ask_email and ask_msg:
        subject = project_data['project_title'] + " Question"
        msg = Message(subject, reply_to=ask_email)
        msg.add_recipient(project_data['project_leaders'][0]['email'])
        msg.html = render_template('mail/project_question.html', msg=ask_msg)

        mail.send(msg)

        flash_msg = "Success! Your question has been submitted, and you should hear from the project manager soon."
        flash(flash_msg, 'success')
        redirect_path = "/" + project_name
        return redirect(redirect_path)

    return render_template('project.html', project_data=project_data, fields=fields)

@app.route('/dev_sync')
def dev_save_and_reload_all_data():
    save_all_data()
    reload_all_data()
    return redirect(redirect_url())

@app.route('/dev_reload')
def dev_reload_all_data():
    reload_all_data()
    return redirect(redirect_url())

def save_all_data():
    projects_controller.write_projects()
    redirects_controller.load_redirects()

def reload_all_data():
    projects_controller.load_projects()
    redirects_controller.load_redirects()

def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')


if __name__ == '__main__':
    app.run()
