#!/usr/bin/python
# -*- coding: utf8 -*-
from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='json_handler',
    version='1.0.1',
    author='Wexxan',
    author_email='WexxanBest@yandex.ru',
    url='https://github.com/WexxanBest/json_handler',
    download_url="http://pypi.python.org/pypi/json_handler/",
    description="Manipulate JSON data or dict values as attributes of an object.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
    packages=find_packages(),
    classifiers=['Topic :: Utilities', 
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'Development Status :: 3 - Alpha',
                 'Programming Language :: Python :: 3.8'],
)