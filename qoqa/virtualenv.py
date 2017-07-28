import venv
import os
import subprocess
import stat

from .build import DATA_DIRECTORY


template_zip = os.path.join(DATA_DIRECTORY, 'template.zip')


class ExtendVenv(venv.EnvBuilder):

    def __init__(self, project_name, *args, **kwargs):
        self._project_name = project_name
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        install default applications
        """
        os.environ['VIRTUAL_ENV'] = context.env_dir
        pip = os.path.join(context.bin_path, 'pip')
        print("[new] Installing pip files: ")
        print("[new] Preparing to install django")
        subprocess.run([pip, 'install', 'django'])
        print("[new] django package installed")
        print('[new] Preparing to install whitenoise')
        subprocess.run([pip, 'install', 'whitenoise'])
        print("[new] whitenoise package installed")
        print("[new] Preparing to install django-debug-toolbar")
        subprocess.run([pip, 'install', 'django-debug-toolbar'])
        print("[new] django-debug-toolbar package installed")
        print("[new] Preparing into install gunicorn")
        subprocess.run([pip, 'install', 'gunicorn'])
        print("[new] gunicorn package installed")
        self._startproject(context)

    def _startproject(self, context):
        """
        Create a new django project
        """
        dj_admin_script = os.path.join(context.bin_path, 'django-admin')
        print("[new] initializing django project")
        subprocess.run([
            dj_admin_script,
            'startproject',
            '--template='+template_zip,
            self._project_name])
        
        print("[new] django project directory created")
        os.chdir(self._project_name)
        with open('__init__.py', 'a'):
            pass
        os.chmod('manage.py', stat.S_IRWXU)


def create(project_name: str):
    """
    create new virtual environment
    """
    env = ExtendVenv(project_name, with_pip=True)
    env.create('env')
