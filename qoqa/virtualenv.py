import venv
import os
import subprocess
import stat


template_zip = os.path.join(os.path.dirname(__file__), 'template.zip')


class ExtendVenv(venv.EnvBuilder):

    def __init__(self, project_name, *args, **kwargs):
        self._project_name = project_name
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        install files from pip
        """
        os.environ['VIRTUAL_ENV'] = context.env_dir
        pip = os.path.join(context.bin_path, 'pip')
        print("Installing pip files: ")
        print("Preparing to install django")
        subprocess.run([pip, 'install', 'django'])
        print("django package installed")
        print('Preparing to install whitenoise')
        subprocess.run([pip, 'install', 'whitenoise'])
        print("whitenoise package installed")
        print("Preparing to install django-debug-toolbar")
        subprocess.run([pip, 'install', 'django-debug-toolbar'])
        print("django-debug-toolbar package installed")
        print("Preparing into install gunicorn")
        subprocess.run([pip, 'install', 'gunicorn'])
        print("gunicorn package installed")
        self._startproject(context)

    def _startproject(self, context):
        """
        Create a new django project
        """
        dj_admin_script = os.path.join(context.bin_path, 'django-admin')
        print("initializing django project")
        subprocess.run([dj_admin_script, 'startproject',
                        '--template='+template_zip,
                        self._project_name])
        print("django project directory created")
        os.chdir(self._project_name)
        os.chmod('manage.py', stat.S_IRWXU)


def create(project_name: str):
    """
    create new virtual environment
    """
    env = ExtendVenv(project_name, with_pip=True)
    env.create('env')
