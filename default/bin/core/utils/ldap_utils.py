import ldap
from core.utils.app_utils import get_env_var
from core.utils.logging_utils import app_logger


ldap_server = get_env_var('LDAP_SERVER_URL')
ldap_bind_dn = get_env_var('LDAP_BIND_DN')
ldap_cred = get_env_var("LDAP_CREDENTIALS")


def ldap_conn():
    con = ldap.initialize(ldap_server)
    con.simple_bind_s(ldap_bind_dn, ldap_cred)
    return con


def get_all_ldap_info(id):
    con = ldap_conn()
    ldap_base = "OU=People,DC=corp,DC=roku"
    ldap_data = con.search_s(ldap_base, ldap.SCOPE_SUBTREE)
    return ldap_data


def get_ldap_info(field, id):
    con = ldap_conn()
    ldap_base = "OU=People,DC=corp,DC=roku"
    query = "({}={})".format(field, id)
    ldap_data = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
    return ldap_data


def get_username(full_name):
    ldap_data = get_ldap_info('cn', full_name)
    name_array = ldap_data[0][1]['sAMAccountName'][0]
    return name_array


def get_manager_fullname(username):
    ldap_data = get_ldap_info('sAMAccountName', username)
    manager_array = ldap_data[0][1]['manager']
    manager_name = manager_array[0].split(',')[0].replace('CN=', '')
    return manager_name


def get_manager(username):
    full_name = get_manager_fullname(username)
    return get_username(full_name)


def ldap_login(username, password):
    conn = ldap.initialize(ldap_server)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    email = '{}@roku.com'.format(username)
    try:
        conn.simple_bind_s(email, password)
        app_logger.info("{} logged in".format(username))
        conn.unbind_s()
        return True
    except:
        app_logger.info("{} failed to log in".format(username))
        return False
