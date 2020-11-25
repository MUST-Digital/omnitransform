#coding: utf-8
import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="omnitransform",
    version="0.3.1",
    author="Martin Kjellberg",
    author_email="martin.kjellberg@mu.st",
    description=(""),
    license="BSD",
    keywords="",
    url="",
    packages=find_packages('src'),
    long_description=read('README.md'),
    package_dir={'': 'omnitransform'},
    install_requires=['openpyxl==3.0.5'],
    python_requires='>=3.7',
)
