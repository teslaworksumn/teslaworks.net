import os
import server_dev
import unittest

def page_exists(response):
    return response.status_code == 200

class TeslaWorksTestCase(unittest.TestCase):

    def setUp(self):
        server_dev.app.config['TESTING'] = True
        self.app = server_dev.app.test_client()
    
    def test_trailing_slash_agnosticism(self):
        response = self.app.get('/lightshow')
        assert page_exists(response)
        
        response = self.app.get('/lightshow/')
        assert page_exists(response)
    

if __name__ == '__main__':
    unittest.main()
