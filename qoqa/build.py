import os
import subprocess
import shutil


def debian():
    """
    Create debian directory with required files
    """
    os.mkdir('debian')
    debian_data = os.path.join(os.path.dirname(__file__), 'debian')
    rules_file = os.path.join(debian_data, 'rules.example')
    control_file = os.path.join(debian_data, 'control.example')
    compat_file = os.path.join(debian_data, 'compat.example')
    postint_file = os.path.join(debian_data, 'postinst.example')
    changelog_file = os.path.join(debian_data, 'changelog.example')
    try:
        shutil.copyfile(rules_file, os.path.join('debian', 'rules'))
        shutil.copyfile(compat_file, os.path.join('debian', 'control'))
        shutil.copyfile(postint_file, os.path.join('debian', 'compat'))
        shutil.copyfile(changelog_file, os.path.join('debian', 'postinst'))
        shutil.copyfile(control_file, os.path.join('debian', 'changelog'))
    except OSError:
        print("[build] Unable to write to current directory")
    except FileNotFoundError as e:
        print("[build]")
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
    Create setup.py file from template
    """
    data_directory = os.path.join(os.path.dirname(__file__), 'data')
    setuppy_file = os.path.join(data_directory, 'setup.py.example')
    with open(setuppy_file, 'r') as f:
        text = f.read().replace('$projectname', os.path.basename(os.getcwd()))
        with open(os.path.join(os.getcwd(), 'setup.py'), 'w') as setup_file:
            setup_file.write(text)
    print('[build] setup.py file created')


def requirements():
    """
    Check whether requirements file exists
    """
    if not os.path.isfile('requirements.txt'):
        print("[build] requirements.txt file does not exist, "
              "create one by activating the relevant emvironment and "
              "typing the command\n"
              "pip freeze > requirements.txt")
    else:
        print('[build] requirements.txt file exists')


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


def dpkg_package():
    """
    Start the build process
    """
