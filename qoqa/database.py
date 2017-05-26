from . import start


def development_postgresql():
    """
    Setup development configurations for postgresql database
    """
    host = input('Database Host: ')
    name = input('Database Name: ')
    user = input('Database User: ')
    password = input("Database Password: ")
    port = input('Database Port: ')
    if '' in [host, name, user, password, port]:
        print("Please enter all database details")
        development_postgresql()
    else:
        start.INIT_PROJECT_CONFIG['DEV_DB'] = {
            'DATABASE': 'postgresql',
            'HOST': host,
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'PORT': port,
        }


def production_postgresql():
    """
    Setup Production configurations for postgresql database
    """
    host = input('Database Host: ')
    name = input('Database Name: ')
    user = input('Database User: ')
    password = input("Database Password: ")
    port = input('Database Port: ')
    if '' in [host, name, user, password, port]:
        print("Please enter all database details")
        development_postgresql()
    else:
        start.INIT_PROJECT_CONFIG['PROD_DB'] = {
            'DATABASE': 'postgresql',
            'HOST': host,
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'PORT': port,
        }
