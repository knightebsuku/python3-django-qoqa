import venv
import os
import subprocess
import stat
import shutil

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
        try:
            print("[qoqa] Installing pip files: ")
            print("[qoqa] Preparing to install django")
            subprocess.run([pip, 'install', 'django'], check=True)
            print("[qoqa] django package installed")
            print('[qoqa] Preparing to install whitenoise')
            subprocess.run([pip, 'install', 'whitenoise'], check=True)
            print("[qoqa] whitenoise package installed")
            print("[qoqa] Preparing to install django-debug-toolbar")
            subprocess.run([pip, 'install', 'django-debug-toolbar'],
                           check=True)
            print("[qoqa] django-debug-toolbar package installed")
            print("[qoqa] Preparing into install gunicorn")
            subprocess.run([pip, 'install', 'gunicorn'], check=True)
            print("[qoqa] gunicorn package installed")
        except subprocess.CalledProcessError as err:
            print("[qoqa] Unable to download pip files, cleaning up")
            print("[qoqa] removing incomplete directory")
            os.chdir("..")
            shutil.rmtree(self._project_name)
            exit()
        else:
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
