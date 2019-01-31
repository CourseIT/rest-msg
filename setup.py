# coding: utf-8
import codecs
import os
from setuptools import setup, find_packages

NAME = "swagger_server"

VERSION = "1.{}".format(os.getenv('BUILD_NUMBER', '0'))

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

this_directory = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="Maintenance",
    author_email="maria.prudyvus@curs.ru",
    url="",
    keywords=["Swagger", "Maintenance"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description=long_description,
    long_description_content_type='text/markdown'
)
