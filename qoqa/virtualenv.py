import venv
import os
import subprocess


class ExtendVenv(venv.EnvBuilder):

    def __init__(self, project_name, *args, **kwargs):
        self._project_name = project_name
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        install files from pip
        """
        os.environ['VIRTUAL_ENV'] = context.env_dir
        activate = os.path.join(context.bin_path, 'pip')
        print("Installing pip files: ")
        print("Preparing to install django")
        subprocess.run([activate, 'install', 'django'])
        print("django package installed")
        print('Preparing to install whitenoise')
        subprocess.run([activate, 'install', 'whitenoise'])
        print("whitenoise package installed")
        print("Preparing to install django-debug-toolbar")
        subprocess.run([activate, 'install', 'django-debug-toolbar'])
        print("django-debug-toolbar package installed")
        print("Preparing into install gunicorn")
        subprocess.run([activate, 'install', 'gunicorn'])
        print("gunicorn package installed")
        self._startproject(context)

    def _startproject(self, context):
        """
        create a new django project
        """
        dj_admin_script = os.path.join(context.bin_path, 'django-admin')
        print("initializing django project")
        subprocess.run([dj_admin_script, 'startproject', self._project_name])
        print("django project directory created")
        os.chdir(self._project_name)


def create_virtualenv(project_name):
    """
    create new virtual environment
    """
    env = ExtendVenv(project_name, with_pip=True)
    env.create('env')
