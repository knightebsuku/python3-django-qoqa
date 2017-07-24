import os
import subprocess
import shutil

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')


def create_changelog():
    """
    Create initial changelog file
    """
    try:
        subprocess.run([
            'dch',
            '--create',
            '--package', os.path.basename(os.getcwd()),
            '--newversion', '0.1.0-1'
        ])
    except subprocess.CalledProcessError as error:
        print("[build] Unable to create changelog file")
        print("[build] {}".format(error))
        exit()


def debian():
    """
    Create debian directory with required files
    """
    os.mkdir('debian')
    debian_data = os.path.join(DATA_DIRECTORY, 'debian')
    rules_file = os.path.join(debian_data, 'rules.example')
    control_file = os.path.join(debian_data, 'control.example')
    compat_file = os.path.join(debian_data, 'compat.example')
    postint_file = os.path.join(debian_data, 'postinst.example')
    try:
        shutil.copyfile(rules_file, os.path.join('debian', 'rules'))
        shutil.copyfile(compat_file, os.path.join('debian', 'compat'))
        shutil.copyfile(postint_file, os.path.join('debian', 'postinst'))
        shutil.copyfile(control_file, os.path.join('debian', 'control'))
        create_changelog()
    except OSError as error:
        print("[build] {}".format(error))
        exit()
    except FileNotFoundError as error:
        print("[build] {}".format(error))
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
    print("[build] debian directory setup")


def python_setup_file():
    """
    Create setup.py file from template and copy to project directory
    """
    setuppy_file = os.path.join(DATA_DIRECTORY, 'setup.py.example')
    with open(setuppy_file, 'r') as f:
        text = f.read().replace('$projectname', os.path.basename(os.getcwd()))
        with open(os.path.join(os.getcwd(), 'setup.py'), 'w') as setup_file:
            setup_file.write(text)
    print('[build] setup.py file created')


def requirements():
    """
    Check whether requirements file exists
    """
    print(
          "[build] create one by activating the relevant virtual environment "
          "and typing the command "
          "pip freeze > requirements.txt")
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
    print('[build] MANIFEST.in file created')


def dpkg():
    """
    Start the build process
    """
    try:
        subprocess.run([
            'dpkg-buildpackage',
            '-us',
            '-uc'
        ])
    except subprocess.CalledProcessError as error:
        print("[build] unable to build project")
        print(['[build] {}'.format(error)])
        exit()
    print("[build] django project built")
