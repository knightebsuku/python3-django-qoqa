import io
import os
import subprocess
import shutil

from colorama import Fore


DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')


def update_changelog(version: str):
    """
    Update changelog file with new version
    """
    try:
        subprocess.run([
            'dch',
            '--newversion',
            version
        ])
    except subprocess.CalledProcessError as error:
        print(Fore.RED + '[qoqa] unable to update version')
        print(Fore.RED + '[qoqa] {}'.format(error))
        exit()


def create_changelog(version: str):
    """
    Create initial changelog file
    """
    try:
            subprocess.run([
                'dch',
                '--create',
                '--package', os.path.basename(os.getcwd()),
                '--newversion', version
            ])
    except subprocess.CalledProcessError as error:
            print(Fore.RED + "[qoqa] Unable to create changelog file")
            print(Fore.RED + "[qoqa] {}".format(error))
            exit()


def debian(version: str):
    """
    Create debian directory with required files
    """
    os.mkdir('debian')
    debian_data = os.path.join(DATA_DIRECTORY, 'debian')
    rules_file = os.path.join(debian_data, 'rules.example')
    control_file = os.path.join(debian_data, 'control.example')
    compat_file = os.path.join(debian_data, 'compat.example')
    postint_file = os.path.join(debian_data, 'postinst.example')
    service_file = os.path.join(debian_data, 'gunicorn.example')
    try:
        project_name = os.path.basename(os.getcwd())
        shutil.copyfile(rules_file, os.path.join('debian', 'rules'))
        shutil.copyfile(compat_file, os.path.join('debian', 'compat'))
        shutil.copyfile(postint_file, os.path.join('debian', 'postinst'))
        shutil.copyfile(control_file, os.path.join('debian', 'control'))
        shutil.copyfile(service_file, os.path.join('debian',
                                                   project_name+'.service'))
        create_changelog(version)
    except OSError as error:
        print(Fore.RED + "[qoqa] {}".format(error))
        exit()
    except FileNotFoundError as error:
        print(Fore.RED + "[qoqa] {}".format(error))
        exit()
    else:
        template_files()


def template_files():
    """
    Read in files in debian directory and replace variables.
    """
    parent_directory = os.path.basename(os.getcwd())
    for filename in os.listdir('debian'):
        with open(os.path.join('debian', filename), 'r+') as f:
            text = f.read().replace('$projectname', parent_directory)
            f.seek(0)
            f.truncate()
            f.write(text)
    print(Fore.GREEN + "[qoqa] debian directory setup")


def python_setup_file():
    """
    Create setup.py file from template and copy to project directory
    """
    setuppy_file = os.path.join(DATA_DIRECTORY, 'setup.py.example')
    with open(setuppy_file, 'r') as f:
        text = f.read().replace('$projectname', os.path.basename(os.getcwd()))
        with open(os.path.join(os.getcwd(), 'setup.py'), 'w') as setup_file:
            setup_file.write(text)
    print(Fore.GREEN + '[qoqa] setup.py file created')


def gunicorn_file():
    """
    Create gunicorn file
    """
    project_directory = os.path.join(os.getcwd(),
                                     os.path.basename(os.getcwd()))
    gunicorn = os.path.join(DATA_DIRECTORY, 'start_gunicorn.example')
    try:
        with open(gunicorn, 'r') as f:
            text = f.read().replace('$projectname',
                                    os.path.basename(os.getcwd()))
            with open(os.path.join(project_directory,
                                   'start_gunicorn'), 'w') as g_file:
                g_file.write(text)
        print(Fore.GREEN + '[qoqa] start_gunicorn file has being created')
    except NotADirectoryError as error:
        print(Fore.RED + '[qoqa] {}'.format(error))
        exit()


def init_file():
    """
    Create init.py to treat project as python package
    """
    project_directory = os.path.join(os.getcwd(),
                                     os.path.basename(os.getcwd()))
    with open(os.path.join(project_directory, '__init__.py'), 'w'):
        pass


def requirements():
    """
    Check whether requirements file exists
    """
    print(Fore.RED + "[qoqa] create one by activating the relevant"
          "virtual environment "
          "and typing the command "
          "pip freeze -l > requirements.txt")
    exit()


def manifest():
    """
    Create manifest file
    """
    data_directory = os.path.join(os.path.dirname(__file__), 'data')
    manifest_file = os.path.join(data_directory, 'MANIFEST.in.example')
    with open(manifest_file, 'r') as f:
        text = f.read().replace('$projectname', os.path.basename(os.getcwd()))
        with open(os.path.join(os.getcwd(), 'MANIFEST.in'), 'w') as manifest:
            manifest.write(text)
    print(Fore.GREEN + '[qoqa] MANIFEST.in file created')


def dpkg(version):
    """
    Start the build process
    """
    try:
        subprocess.run([
            'dch',
            '-r',
            version
        ], check=True)
    except subprocess.CalledProcessError as error:
        print(Fore.RED + "[qoqa] unable to release project")
        print(Fore.RED + "[qoqa] {}".format(error))
        exit()
    try:
        subprocess.run([
            'dpkg-buildpackage',
            '-us',
            '-uc'
        ], check=True)
    except subprocess.CalledProcessError as error:
        print(Fore.RED + "[qoqa] unable to releaseproject")
        print(Fore.RED + '[qoqa] {}'.format(error))
        exit()
    print(Fore.GREEN + "[qoqa] django project built")


def django_app_data():
    """
    Find all python packages within django project and treat
    them as a django app and add them to setuptools package_data
    """
    valid_django_apps = []
    project_directory = os.path.basename(os.getcwd())
    apps = os.walk(os.path.basename(os.getcwd()))
    app_folders = next(apps)[1]
    for folder in app_folders:
        if folder == project_directory:
            continue
        if os.path.isfile(os.path.join(project_directory,
                                       folder, '__init__.py')):
            print(Fore.GREEN + '[qoqa] found django app {}'.format(folder))
            print(Fore.GREEN + '[qoqa] adding templates and static files')
            valid_django_apps.append('{0}/templates/{0}/*.djhtml'.format(folder,))
            valid_django_apps.append('{0}/static/{0}/css/*.css'.format(folder,))
            valid_django_apps.append('{0}/static/{0}/js/*.js'.format(folder,))
            valid_django_apps.append('{0}/static/{0}/img/*.png'.format(folder,))
    if valid_django_apps:
        package_data = {project_directory: valid_django_apps}
        with open('setup.py', 'r+') as setup_file:
            new_setup_file = io.StringIO()
            for line in setup_file:
                if line.startswith('PACKAGE_DATA'):
                    new_setup_file.write('PACKAGE_DATA = {}\n\n'.
                                         format(package_data))
                else:
                    new_setup_file.write(line)
            setup_file.seek(0)
            setup_file.write(new_setup_file.getvalue())
            new_setup_file.close()
    print(Fore.GREEN + '[qoqa] collected and setup files')
