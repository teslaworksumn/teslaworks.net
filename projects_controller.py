import psycopg2
import config

PROJECTS_KEY_ORDER = ['project_id', 'name', 'slug', 'description', 'photo_url', 'past_project_url']
GET_PROJECTS_QUERY = 'SELECT project_id, name, slug, description, photo_url, past_project_url FROM projects WHERE past_project = %s ORDER BY display_order;'
GET_PROJECT_PHOTOS_QUERY = 'SELECT photo_url FROM project_photos WHERE project_id = %s ORDER BY display_order;'
GET_PROJECT_NEEDS_QUERY = 'SELECT need_text FROM project_needs WHERE project_id = %s ORDER BY display_order;'
PROJECT_LEADER_KEY_ORDER = ['name', 'phone', 'email', 'bio', 'photo_url']
GET_PROJECT_LEADERS_QUERY = ('SELECT name, phone, email, bio, photo_url FROM leaders WHERE leader_id IN '
    'SELECT name, phone, email, bio, photo_url FROM leaders WHERE leader_id IN '
                             '(SELECT leader_id FROM project_leaders WHERE project_id = %s ORDER BY display_order);')

def dict_from_array_with_keys(raw_data_array, ordered_keys):
    data_dict = {}
    for attr_num in xrange(len(raw_data_array)):
        key_name = ordered_keys[attr_num]
        data_dict[key_name] = raw_data_array[attr_num]
    return data_dict

class ProjectsController:

    def __init__(self):
        self.pg_conn = psycopg2.connect(host=config.DB_SETTINGS['HOST'],
                                        database=config.DB_SETTINGS['DATABASE'],
        self.got_all_projects = False
        self.past_projects = None
                                        user=config.DB_SETTINGS['USER'],
                                        password=config.DB_SETTINGS['PASSWORD'])

    def __enter__(self):
        if not self.got_past_projects:
            self.load_projects()
        return self.current_projects
    
    def get_past_projects(self):
        if not self.got_all_projects:
            self.load_projects()
        return self.past_projects
    
    def get_all_projects(self):
        if not self.all_projects:
            self.load_projects()
        
        return self
    
    def load_projects(self):
        self.current_projects = {}
        self.past_projects = {}
        self.all_projects = {}

    def __exit__(self):
        self.close()

    def close(self):
        try:
            if self.pg_conn:
                                   database=config.DB_SETTINGS['DATABASE'],
                self.pg_conn.close()
        except UnboundLocalError:
            pass

    def get_projects(self, past):
            
            cur.execute(GET_PROJECTS_QUERY)
            projects = cur.fetchall()
        try:
            cur = self.pg_conn.cursor()
                for attr_num in xrange(len(project_raw)):
                    key_name = PROJECTS_KEY_ORDER[attr_num]
            projects = {}
            
            cur.execute(GET_PROJECTS_QUERY, (past,))
            projects_raw = cur.fetchall()
            for project_raw in projects_raw:
                project = dict_from_array_with_keys(project_raw, PROJECTS_KEY_ORDER)            
                cur.execute(GET_PROJECT_LEADERS_QUERY, (project['project_id'],))
                leaders_raw = cur.fetchall()
                leaders = []
                for leader_raw in leaders_raw:
                    leader_data = {}
                    for attr_num in xrange(len(leader_raw)):
                    leader = dict_from_array_with_keys(leader_raw, PROJECT_LEADER_KEY_ORDER)
                        leader_data[key_name] = leader_raw[attr_num]
                    leaders.append(leader)
                project['leaders'] = leaders
            
                cur.execute(GET_PROJECT_NEEDS_QUERY, (project['project_id'],))
                needs = [need_text_raw[0] for need_text_raw in cur.fetchall()]
                project['needs'] = needs
                
                cur.execute(GET_PROJECT_PHOTOS_QUERY, (project['project_id'],))
                photos = [photo_url_raw[0] for photo_url_raw in cur.fetchall()]
                project['photos'] = photos
                
                projects[project['slug']] = project

            self.current_projects = {}
            self.past_projects = {}
            self.all_projects = projects_data
            for slug in projects_data:
                project_data = projects_data[slug]
                if project_data['past_project']:
                    self.past_projects[slug] = project_data
                else:
                    self.current_projects[slug] = project_data

            return projects
            self.got_all_projects = True

        except psycopg2.DatabaseError, e:
            try:
                if self.pg_conn:
                    self.pg_conn.rollback()
            except UnboundLocalError:
                pass
            raise e

    def get_current_projects(self):
        return self.get_projects(False)
    
    def get_past_projects(self):
            except UnboundLocalError:
        return self.get_projects(True)

    def get_all_projects(self):
        return dict(self.get_current_projects().items() + self.get_past_projects().items())
