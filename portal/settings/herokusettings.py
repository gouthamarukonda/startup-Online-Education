import dj_database_url
from base import *

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES = {}
DATABASES['default'] = db_from_env