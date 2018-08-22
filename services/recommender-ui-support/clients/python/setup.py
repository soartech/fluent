# coding: utf-8

"""
    Recommender UI Support Service API

    This API is used to interact with the data stored in the Recommender UI Support Service database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "recommenderuisupportclient"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Recommender UI Support Service API",
    author_email="",
    url="",
    keywords=["Swagger", "Recommender UI Support Service API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    This API is used to interact with the data stored in the Recommender UI Support Service database.  # noqa: E501
    """
)
