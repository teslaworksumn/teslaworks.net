import config

def mixpanel_token():
    if config.MIXPANEL_SUPPRESS_SEND:
        return None

    return config.MIXPANEL_TOKEN

def cdn_url(url):
    return config.CDN_SCHEME + '//' + config.CDN_DOMAIN + '/' + config.CDN_VERSION + '/' + url

def email_address(email):
    if app.debug or app.testing:
        return config.DEBUG_EMAIL
    return email
