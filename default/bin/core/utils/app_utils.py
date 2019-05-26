import os


def check_local_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


# Get env var from opsworks
def get_env_var(env_name):
    f = open(os.environ['ENV_DIR'] + env_name)
    for line in iter(f):
        var = line.replace("\n", "")
        return var
    f.close()


def get_theme(type='None'):
    if type == 'path':
        result = 'themes/' + os.environ.get('THEME')
    else:
        result = os.environ.get('THEME')
    return result
