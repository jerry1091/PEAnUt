import logging
from os.path import dirname, abspath
import os
from core.utils.app_utils import check_local_dir, get_env_var
from mods.config import app_name, db_type, db_name


# Env directory
app_path = dirname(dirname(dirname(abspath(__file__))))
env_dir = '{}/env/'.format(app_path)

db_path = '{}/database'.format(app_path)
check_local_dir(db_path)
database = '{}/{}'.format(db_path, db_name)

os.environ['ENV_DIR'] = env_dir

if os.environ.get('THEME') is None:
    os.environ['THEME'] = 'limitless'

# Logging setup.
log_path = '{}/log/'.format(app_path)
log_format = logging.Formatter('%(asctime)s -- %(levelname)s : %(message)s')
check_local_dir(log_path)

# Other settings
os.environ['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    if db_type == 'sqlite':
        db_path = '{}/database'.format(app_path)
        check_local_dir(db_path)
        database = '{}/{}'.format(db_path, db_name)
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(database)
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    elif db_type == 'mysql':
        db_user = get_env_var('DB_USER')
        db_pass = get_env_var('DB_PASS')
        db_host = get_env_var('DB_HOST')
        db_name = get_env_var('DB_NAME')
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_pass, db_host, db_name)
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False