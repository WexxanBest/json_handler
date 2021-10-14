#!/usr/bin/python
# -*- coding: utf8 -*-
from setuptools import setup, find_packages


setup(
    name='json_handler',
    version='1.0',
    author='Wexxan',
    author_email='WexxanBest@yandex.ru',
    url='https://github.com/WexxanBest/json_handler',
    download_url="http://pypi.python.org/pypi/json_handler/",
    description="Manipulate JSON data or dict values as attributes of an object.",
    install_requires=[],
    packages=find_packages(),
    classifiers=['Topic :: Utilities', 
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                 'Programming Language :: Python :: 3.8'],
)