from colorama import Fore


def create(status):
    """
    Set up database for development and production
    """
    print(Fore.GREEN + f"Avaliable Databases for {status}")
    print(Fore.GREEN + "1 - sqlite3")
    print(Fore.GREEN + "2 - postgresql")
    while True:
        db = input(Fore.GREEN + f"{status} Database [1]: ")
        if db == "1" or db == "":
            return {"DATABASE": "sqlite3", "NAME": f"{status}.sqlite3"}
        elif db == "2":
            return postgresql()
        else:
            print(Fore.RED + "[qoqa] Unknown database selection")


def postgresql():
    """
    Configure Postgres database
    """
    while True:
        host = input(Fore.GREEN + "Database Host: ")
        name = input(Fore.GREEN + "Database Name: ")
        port = input(Fore.GREEN + "Database Port: ")
        user = input(Fore.GREEN + "Database User: ")
        password = input(Fore.GREEN + "Database Password: ")
        if "" in [host, name, user, password, port]:
            print(Fore.RED + "Please enter all database details")
        if not port.isdigit():
            print(Fore.RED + "Port is not a number")
        else:
            return {
                "DATABASE": "postgresql",
                "HOST": host,
                "NAME": name,
                "USER": user,
                "PASSWORD": password,
                "PORT": port,
            }
