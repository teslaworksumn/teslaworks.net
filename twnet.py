from flask import Flask, request, url_for, render_template, flash, redirect, abort
from jinja2 import evalcontextfilter, Markup, escape
from flask_mail import Mail, Message
from raven.contrib.flask import Sentry, Client
from projects_controller import ProjectsController
from redirects_controller import RedirectsController
import config
import re
import strings
import atexit

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.url_map.strict_slashes = False
app.config.update(config.APP_CONFIG)

app.config.update(config.MAIL_SETTINGS)
mail = Mail(app)

app.config.update(config.SENTRY_SETTINGS)
sentry = Sentry(app)

projects_controller = ProjectsController()
redirects_controller = RedirectsController()

def close_db_conn():
    projects_controller.close()

atexit.register(close_db_conn)

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
    return render_template('404.html', mixpanel_token=mixpanel_token()), 404

@app.route('/')
def index():
    current_projects = projects_controller.get_current_projects()
    past_projects = projects_controller.get_past_projects()
    return render_template('index.html', current_projects=current_projects, past_projects=past_projects, mixpanel_token=mixpanel_token())

@app.route('/start', methods=['GET', 'POST'])
def start_project():
    if request.method == 'GET':
        return render_template('start.html', form={}, errors={}, mixpanel_token=mixpanel_token())

    form = request.form
    errors = {}

    if not form['name']:
        errors['name'] = strings.ERROR_NO_NAME

    if not form['email']:
        errors['email'] = strings.ERROR_NO_EMAIL_TO_GET_AHOLD

    if not form['ptitle']:
        errors['ptitle'] = strings.ERROR_NO_PROJ_TITLE
    
    if not form['desc']:
        errors['desc'] = strings.ERROR_NO_PROJ_DESC

    if not errors:
        subject = strings.SUBJ_PROJ_NEW % form.get('ptitle')
        msg = Message(subject)
        msg.add_recipient(email_address(config.CONTACT_EMAIL))
        msg.html = render_template('mail/start.html', form=form)
        msg.body = render_template('mail/start.txt', form=form)
        
        mail.send(msg)

        flash(strings.SUCCESS_APP_SUBMITTED, 'success')
        return redirect(url_for('index'))

    flash(strings.ERROR_NOT_SUBMITTED, 'danger')
    return render_template('start.html', form=form, errors=errors, mixpanel_token=mixpanel_token())

@app.route('/<dynamic>', methods=['GET', 'POST'])
def dynamic(dynamic):

    # First, test if if it's a project
    projects = projects_controller.get_all_projects()
    if dynamic in projects:
        project_data = projects[dynamic]
        past_project_url = project_data.get('past_project_url')
        if past_project_url:
            # The project is over, we should redirect to the post
            return redirect(past_project_url)
        else:
          return render_project(dynamic, project_data)

    redirects = redirects_controller.get_redirects()
    if dynamic in redirects:
        return redirect(redirects[dynamic])

    abort(404)

def render_project(project_name, project_data):
    if request.method == 'GET':
        return render_template('project.html', project_data=project_data, form={}, errors={}, mixpanel_token=mixpanel_token())

    form = request.form
    errors = {}

    if 'join_email' in form:
        if not form['join_email']:
            errors['join_email'] = strings.ERROR_NO_EMAIL_TO_GET_AHOLD
        
        if not errors:
            subject = strings.SUBJ_PROJ_JOIN_REQUESTED % project_data['name']
            msg = Message(subject)
            msg.add_recipient(email_address(project_data['leaders'][0]['email']))
            msg.html = render_template('mail/join_project.html', form=form)
            msg.body = render_template('mail/join_project.txt', form=form)
    
            mail.send(msg)
    
            flash_msg = strings.SUCCESS_PROJ_JOINED % project_data['name']
            flash(flash_msg, 'success')
            return redirect('/' + project_name)

    if 'ask_msg' in form:
        if not form['ask_msg']:
            errors['ask_msg'] = strings.ERROR_DONT_FORGET_MSG

        if not form['ask_email']:
            errors['ask_email'] = strings.ERROR_NO_EMAIL_TO_ANSWER

        if not errors:
            subject = strings.SUBJ_PROJ_QUESTION % project_data['name']
            msg = Message(subject, reply_to=form.get('ask_email'))
            msg.add_recipient(email_address(project_data['leaders'][0]['email']))
            msg.html = render_template('mail/project_question.html', form=form)
            msg.body = render_template('mail/project_question.txt', form=form)

            mail.send(msg)

            flash_msg = strings.SUCCESS_MESSAGE_SUBMITTED
            flash(flash_msg, 'success')
            return redirect('/' + project_name)

    flash(strings.ERROR_NOT_SUBMITTED, 'danger')
    return render_template('project.html', project_data=project_data, form=form, errors=errors, mixpanel_token=mixpanel_token())

@app.route('/dev_sync')
def dev_save_and_reload_all_data():
    save_all_data()
    reload_all_data()
    return redirect(redirect_url())

@app.route('/dev_reload')
def dev_reload_all_data():
    reload_all_data()
    return redirect(redirect_url())

def mixpanel_token():
    if config.MIXPANEL_SUPPRESS_SEND:
        return None

    return config.MIXPANEL_TOKEN

def save_all_data():
    projects_controller.write_projects()
    redirects_controller.load_redirects()

def reload_all_data():
    projects_controller.load_projects()
    redirects_controller.load_redirects()

def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')

def email_address(email):
    if app.debug or app.testing:
        return config.DEBUG_EMAIL
    return email

if __name__ == '__main__':
    app.run()
