# coding: utf-8

"""
    CASS Graph Library

    This Library is used to interact with CASS Competency Competencies from a CASS Framework using a directed graph.

"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "cass-graph"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["requests"]

setup(
    name=NAME,
    version=VERSION,
    description="Graph functions for CASS Frameworks",
    author_email="",
    url="",
    keywords=["CASS GRAPH"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="This Library is used to interact with CASS Competency Competencies from a CASS Framework using a directed graph."
)
