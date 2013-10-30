import psycopg2
import config

GET_REDIRECTS_QUERY = 'SELECT slug, url FROM redirects;'

class RedirectsController:
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

    def get_redirects(self):
        try:
            cur = self.pg_conn.cursor()
            redirects = {}
            
            cur.execute(GET_REDIRECTS_QUERY)
            redirects_raw = cur.fetchall()
            for redirect_raw in redirects_raw:
                redirects[redirect_raw[0]] = redirect_raw[1];
                
            return redirects

        except psycopg2.DatabaseError, e:
            try:
                if self.pg_conn:
                    self.pg_conn.rollback()
            except UnboundLocalError:
                pass
            raise e
