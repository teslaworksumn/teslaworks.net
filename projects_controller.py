import psycopg2
import config

PROJECTS_KEY_ORDER = ['id', 'name', 'slug', 'description', 'photo_url', 'past_project']
GET_PROJECTS_QUERY = 'SELECT project_id, name, slug, description, photo_url, past_project FROM projects ORDER BY display_order;'
GET_PROJECT_PHOTOS_QUERY = 'SELECT photo_url FROM project_photos WHERE project_id = %s ORDER BY display_order;'
GET_PROJECT_NEEDS_QUERY = 'SELECT need_text FROM project_needs WHERE project_id = %s ORDER BY display_order;'
PROJECT_LEADER_KEY_ORDER = ['name', 'phone', 'email', 'bio', 'photo_url']
GET_PROJECT_LEADERS_QUERY = (
    'SELECT name, phone, email, bio, photo_url FROM leaders WHERE leader_id IN '
        '(SELECT leader_id FROM project_leaders WHERE project_id = %s ORDER BY display_order);'
)

class ProjectsController:
    def __init__(self):
        self.current_projects = None
        self.got_past_projects = False
        self.got_all_projects = False
        self.past_projects = None
        self.all_projects = None
        self.pg_conn = psycopg2.connect(host=config.DB_SETTINGS['HOST'],
                                        database=config.DB_SETTINGS['DATABASE'],
                                        user=config.DB_SETTINGS['USER'],
                                        password=config.DB_SETTINGS['PASSWORD'])

    def __enter__(self):
        return self

    def __exit__(self):
        try:
            if self.pg_conn:
                self.pg_conn.close()
        except UnboundLocalError:
            pass

    def close(self):
        self.__exit__()

    def get_current_projects(self):
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
        return self.all_projects
    
    def load_projects(self):
        self.current_projects = {}
        self.past_projects = {}
        self.all_projects = {}

        try:
            cur = self.pg_conn.cursor()
            projects_data = {}
            
            cur.execute(GET_PROJECTS_QUERY)
            projects = cur.fetchall()
            for project_raw in projects:
                project_data = {}
                for attr_num in xrange(len(project_raw)):
                    key_name = PROJECTS_KEY_ORDER[attr_num]
                    project_data[key_name] = project_raw[attr_num]
            
                cur.execute(GET_PROJECT_LEADERS_QUERY, (project_data['id'],))
                leaders_raw = cur.fetchall()
                leaders_data = []
                for leader_raw in leaders_raw:
                    leader_data = {}
                    for attr_num in xrange(len(leader_raw)):
                        key_name = PROJECT_LEADER_KEY_ORDER[attr_num]
                        leader_data[key_name] = leader_raw[attr_num]
                    leaders_data.append(leader_data)
                project_data['leaders'] = leaders_data
            
                cur.execute(GET_PROJECT_NEEDS_QUERY, (project_data['id'],))
                needs = [text_holder[0] for text_holder in cur.fetchall()]
                project_data['needs'] = needs
                
                cur.execute(GET_PROJECT_PHOTOS_QUERY, (project_data['id'],))
                photos = [url_holder[0] for url_holder in cur.fetchall()]
                project_data['photos'] = photos
                
                projects_data[project_data['slug']] = project_data

            self.current_projects = {}
            self.past_projects = {}
            self.all_projects = projects_data
            for slug in projects_data:
                project_data = projects_data[slug]
                if project_data['past_project']:
                    self.past_projects[slug] = project_data
                else:
                    self.current_projects[slug] = project_data

            self.got_past_projects = True
            self.got_all_projects = True

        except psycopg2.DatabaseError, e:
            try:
                if self.pg_conn:
                    self.pg_conn.rollback()
            except UnboundLocalError:
                pass
            raise e
