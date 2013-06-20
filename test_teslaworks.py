import server_dev

def page_exists(response):
    return response.status_code == 200

def test_trailing_slash_agnosticism():
    server_dev.app.config['TESTING'] = True
    app = server_dev.app.test_client()
    
    response_no_slashes = app.get('/lightshow')
    assert page_exists(response_no_slashes)
    
    response_with_slashes = app.get('/lightshow/')
    assert page_exists(response_with_slashes)
