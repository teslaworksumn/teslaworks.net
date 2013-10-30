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
        self.pg_conn = psycopg2.connect(host=config.DB_SETTINGS['HOST'],
                                        database=config.DB_SETTINGS['DATABASE'],
                                        user=config.DB_SETTINGS['USER'],
                                        password=config.DB_SETTINGS['PASSWORD'])

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def close(self):
        try:
            if self.pg_conn:
                self.pg_conn.close()
        except UnboundLocalError:
            pass

    def get_all_projects(self):
        try:
            cur = self.pg_conn.cursor()
            projects = {}
            
            cur.execute(GET_PROJECTS_QUERY)
            projects_raw = cur.fetchall()
            for project_raw in projects_raw:
                project = dict_from_array_with_keys(project_raw, PROJECTS_KEY_ORDER)            
                cur.execute(GET_PROJECT_LEADERS_QUERY, (project['id'],))
                leaders_raw = cur.fetchall()
                leaders = []
                for leader_raw in leaders_raw:
                    leader = dict_from_array_with_keys(leader_raw, PROJECT_LEADER_KEY_ORDER)
                    leaders.append(leader)
                project['leaders'] = leaders
            
                cur.execute(GET_PROJECT_NEEDS_QUERY, (project['id'],))
                needs = [need_text_raw[0] for need_text_raw in cur.fetchall()]
                project['needs'] = needs
                
                cur.execute(GET_PROJECT_PHOTOS_QUERY, (project['id'],))
                photos = [photo_url_raw[0] for photo_url_raw in cur.fetchall()]
                project['photos'] = photos
                
                projects[project['slug']] = project

            return projects

        except psycopg2.DatabaseError, e:
            try:
                if self.pg_conn:
                    self.pg_conn.rollback()
            except UnboundLocalError:
                pass
            raise e

    def get_current_projects(self):
        return {slug: project for (slug, project) in self.get_all_projects().iteritems() if not project['past_project']}
    
    def get_past_projects(self):
        return {slug: project for (slug, project) in self.get_all_projects().iteritems() if project['past_project']}
