from . import qoqa
from colorama import Fore


def setup():
    """
    Configure database details
    """
    print(Fore.GREEN + 'Avaliable Databases')
    print(Fore.GREEN + '1 - sqlite3')
    print(Fore.GREEN + '2 - postgresql')
    dev_db = input(Fore.GREEN + "Development Database [1]: ")
    if dev_db == '' or dev_db == '1':
        qoqa.INIT_PROJECT_CONFIG['DEV_DB'] = {
            'DATABASE': 'sqlite3',
            'NAME': 'development_db.sqlite3'
        }
    elif dev_db == '2':
        development_postgresql()
    else:
        print(Fore.RED + "[qoqa] Unknown database selection")
        setup()
    prod_db = input(Fore.GREEN + "Production Database[1]: ")
    if prod_db == '' or prod_db == '1':
        qoqa.INIT_PROJECT_CONFIG['PROD_DB'] = {
            'DATABASE': 'sqlite3',
            'NAME': 'production_db.sqlite3'
        }
    elif prod_db == '2':
        production_postgresql()
    else:
        print(Fore.RED + "Unknown database or database is not supported")
        setup()
    return prod_db


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
