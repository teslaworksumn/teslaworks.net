import json
import os

class RedirectsController:

    def __init__(self, data_dir):
        self.redirects_data_file_path = os.path.join(data_dir, 'redirects.json')
        self.redirects = None

    def get_redirects(self):
        if not self.redirects:
            self.load_redirects()
        
        return self.redirects

    def set_redirects(self, redirects):
        self.redirects = redirects
        self.write_redirects()

    def load_redirects(self):
        self.redirects = {}
        with open(self.redirects_data_file_path, 'r') as f:
            self.redirects = json.load(f)

    def write_redirects(self):
        with open(self.redirects_data_file_path, 'w') as f:
            json.dump(data, f)
