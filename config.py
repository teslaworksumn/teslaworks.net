DATA_DIR = 'data'
SECRET_KEY = '6C863A81-5C37-47BE-9D7D-362F073F7BE7'

CONTACT_EMAIL = 'officers@teslaworks.net'
DEBUG_EMAIL = 'webmaster@teslaworks.net'

APP_CONFIG = {
  'DEBUG': False,
  'TESTING': False
}

MAIL_SETTINGS = {
  'MAIL_SERVER': 'smtp.mailgun.org',
  'MAIL_PORT': '25',
  'MAIL_USE_TLS': False,
  'MAIL_USERNAME': 'postmaster@mailer.teslaworks.net',
  'MAIL_PASSWORD': '0b9--9zv2aq8',
  'MAIL_DEFAULT_SENDER': 'twnet@mailer.teslaworks.net',
  'MAIL_SUPPRESS_SEND': False
}

SENTRY_SETTINGS = {
  'SENTRY_DSN': 'https://your.dsn.goes/here/3'
}
