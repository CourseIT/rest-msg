# coding: utf-8
import codecs
import os
from setuptools import setup, find_packages

NAME = "rest-msg"

VERSION = "1.{}".format(os.getenv('BUILD_NUMBER', '0'))

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ['connexion', 'connexion[swagger-ui]', 'Flask-CORS', 'Flask-SQLAlchemy',
            'python-dotenv', 'python_dateutil', 'gunicorn', 'psycopg2']

this_directory = os.path.abspath(os.path.dirname(__file__))

setup(
    name=NAME,
    version=VERSION,
    description="Maintenance",
    author="Maria Prudyvus",
    author_email="maria.prudyvus@curs.ru",
    url="https://artifactory.corchestra.ru/artifactory/course-med/rest-msg/",
    keywords=["Swagger", "Maintenance"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'swagger': ['swagger_server/swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    Сервер для публикации профилактических работ
    """
)
