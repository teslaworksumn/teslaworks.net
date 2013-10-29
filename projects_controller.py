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

def dict_from_array_with_keys(raw_data_array, ordered_keys):
    data_dict = {}
    for attr_num in xrange(len(raw_data_array)):
        key_name = ordered_keys[attr_num]
        data_dict[key_name] = raw_data_array[attr_num]
    return data_dict

class ProjectsController:

    def __init__(self):
        self.current_projects = None
        self.projects_loaded = False
        self.past_projects = None
        self.all_projects = None

    def get_current_projects(self):
        if not self.projects_loaded:
            self.load_projects()
        return self.current_projects
    
    def get_past_projects(self):
        if not self.projects_loaded:
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
            con = psycopg2.connect(host=config.DB_SETTINGS['HOST'],
                                   database=config.DB_SETTINGS['DATABASE'],
                                   user=config.DB_SETTINGS['USER'],
                                   password=config.DB_SETTINGS['PASSWORD'])
            cur = con.cursor()

            projects_data = {}
            
            cur.execute(GET_PROJECTS_QUERY)
            projects = cur.fetchall()
            for project_raw in projects:
                project_data = dict_from_array_with_keys(project_raw, PROJECTS_KEY_ORDER)            
                cur.execute(GET_PROJECT_LEADERS_QUERY, (project_data['id'],))
                leaders_raw = cur.fetchall()
                leaders_data = []
                for leader_raw in leaders_raw:
                    leader_data = dict_from_array_with_keys(leader_raw, PROJECT_LEADER_KEY_ORDER)
                    leaders_data.append(leader_data)
                project_data['leaders'] = leaders_data
            
                cur.execute(GET_PROJECT_NEEDS_QUERY, (project_data['id'],))
                needs = [need_text_raw[0] for need_text_raw in cur.fetchall()]
                project_data['needs'] = needs
                
                cur.execute(GET_PROJECT_PHOTOS_QUERY, (project_data['id'],))
                photos = [photo_url_raw[0] for photo_url_raw in cur.fetchall()]
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

            self.projects_loaded = True

        except psycopg2.DatabaseError, e:
            try:
                if con:
                    con.rollback()
            except UnboundLocalError:
                pass
            raise e

        finally:
            try:
                if con:
                    con.close()
            except UnboundLocalError:
                pass

