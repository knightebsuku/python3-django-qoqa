import configparser

INIT_PROJECT_CONFIG = {}


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
        INIT_PROJECT_CONFIG['DEV_DB'] = {
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
        INIT_PROJECT_CONFIG['PROD_DB'] = {
            'DATABASE': 'postgresql',
            'HOST': host,
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'PORT': port,
        }


def project_name():
    name = input("Project Name: ")
    if name == "":
        print("Please enter a project name")
        project_name()
    else:
        INIT_PROJECT_CONFIG['PROJECT_NAME'] = name


def database():
    dev_db = input("Development Database[sqlite]: ")
    if dev_db == '':
        dev_db = 'sqlite'
        INIT_PROJECT_CONFIG['DEV_DB'] = {
            'Database': dev_db,
            'name': 'development_db.sqlite3'
        }
    elif dev_db == 'postgresql':
        development_postgresql()

    prod_db = input("Production Database[sqlite]: ")
    if prod_db == '':
        prod_db = 'sqlite'
        INIT_PROJECT_CONFIG['PROD_DB'] = {
            'Database': prod_db,
            'name': 'production_db.sqlite3'
        }
    elif prod_db == 'postgresql':
        production_postgresql()
    print("Database settings confugured")


def create_config():
    """
    Create configuration file for django project
    """
    print("Creating configuration file")
    config = configparser.ConfigParser()
    config['STATUS'] = {
        'Prodcution': False
    }
    dev = INIT_PROJECT_CONFIG['DEV_DB']
    prod = INIT_PROJECT_CONFIG['PROD_DB']
    config['DEVELOPMENT_DATABSE'] = {k: v for k, v in dev.items()}
    config['PRODUCTION_DATABASE'] = {k: v for k, v in prod.items()}
    config['ALLOWED_HOSTS'] = {'Host': '127.0.0.1,locahost'}
    with open(INIT_PROJECT_CONFIG['PROJECT_NAME']+'.cfg', 'w') as project_file:
        config.write(project_file)
    print('Configuration file has been created')


def startproject():
    """
    Launch interactive console
    """
    print("Configure New Django Project")
    project_name()
    database()
    create_config()

