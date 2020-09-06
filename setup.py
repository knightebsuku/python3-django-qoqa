from setuptools import setup, find_packages

setup(
    name="python3-django-qoqa",
    version="1.0.0",
    packages=find_packages(),
    scripts=["django-qoqa.py"],
    package_data={
        "qoqa": [
            "data/debian/*.example",
            "data/MANIFEST.in.example",
            "data/setup.py.example",
            "data/start_gunicorn.example",
            "data/template.zip",
        ]
    },
    author="Lunga Mthembu",
    author_email="stumenz.complex@gmail.com",
    description="Commandline application to package django projects",
    license="GPLv3",
    keywords="python3 django virtualenv",
    url="https://github.com/ebsuku/python3-django-qoqa",
)
