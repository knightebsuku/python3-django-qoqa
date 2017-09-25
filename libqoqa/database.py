from . import qoqa
from colorama import Fore


def setup():
    """
    Configure database details
    """
    dev_db = input(Fore.GREEN + "Development Database[sqlite3]: ")
    if dev_db == '' or dev_db == 'sqlite3':
        qoqa.INIT_PROJECT_CONFIG['DEV_DB'] = {
            'DATABASE': 'sqlite3',
            'NAME': 'development_db.sqlite3'
        }
    elif dev_db == 'postgresql':
        development_postgresql()
    else:
        print(Fore.RED + "[qoqa] Unknown database or database is not supported")
        setup()
    prod_db = input(Fore.GREEN + "Production Database[sqlite3]: ")
    if prod_db == '' or prod_db == 'sqlite3':
        qoqa.INIT_PROJECT_CONFIG['PROD_DB'] = {
            'DATABASE': 'sqlite3',
            'NAME': 'production_db.sqlite3'
        }
    elif prod_db == 'postgresql':
        production_postgresql()
    else:
        print(Fore.RED + "Unknown database or database is not supported")
        setup()


def development_postgresql():
    """
    Setup development configurations for postgresql database
    """
    host = input(Fore.GREEN + 'Database Host: ')
    name = input(Fore.GREEN + 'Database Name: ')
    port = input(Fore.GREEN + 'Database Port: ')
    user = input(Fore.GREEN + 'Database User: ')
    password = input(Fore.GREEN + "Database Password: ")
    if '' in [host, name, user, password, port]:
        print(Fore.RED + "Please enter all database details")
        development_postgresql()
    else:
        qoqa.INIT_PROJECT_CONFIG['DEV_DB'] = {
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
    host = input(Fore.GREEN + 'Database Host: ')
    name = input(Fore.GREEN + 'Database Name: ')
    user = input(Fore.GREEN + 'Database User: ')
    password = input(Fore.GREEN + "Database Password: ")
    port = input(Fore.GREEN + 'Database Port: ')
    if '' in [host, name, user, password, port]:
        print(Fore.RED + "Please enter all database details")
        development_postgresql()
    else:
        qoqa.INIT_PROJECT_CONFIG['PROD_DB'] = {
            'DATABASE': 'postgresql',
            'HOST': host,
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'PORT': port,
        }
