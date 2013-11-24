import config

def mixpanel_token():
    if config.MIXPANEL_SUPPRESS_SEND:
        return None

    return config.MIXPANEL_TOKEN

def email_address(email):
    if app.debug or app.testing:
        return config.DEBUG_EMAIL
    return email
