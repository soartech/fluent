# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "learner_inferences_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Learner API",
    author_email="",
    url="",
    keywords=["Swagger", "Learner API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['learner_inferences_server=learner_inferences_server.__main__:main']},
    long_description="""\
    This API is used to interact with the data stored in the TLA Learner Profile database.
    """
)

