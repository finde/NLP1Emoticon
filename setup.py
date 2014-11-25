#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of NLP1Emoticon.
# https://github.com/finde/NLP1Emoticon

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 nlp1_emoticon_team finde.xumara@gmail.com


from setuptools import setup, find_packages
from Code import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]


setup(
    name='NLP1Emoticon',
    version=__version__,
    description='an incredible python package',
    long_description='''
an incredible python package
''',
    keywords='emoticons, predictor',
    author='nlp1_emoticon_team',
    author_email='finde.xumara@gmail.com',
    url='https://github.com/finde/NLP1Emoticon',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        'numpy>=1.9.0',
        'tweepy>=2.3.0',
        'ftfy>=3.3.0',
        'nltk>=3.0.0',
        'language_check>=0.7',
        'progressbar>=2.2',
        'flask>=0.10.1',
        'flask-appconfig>=0.9.1',
        'flask-bootstrap>=3.3.0.1',
        'Jinja2>=2.7.3'
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'NLP1Emoticon=NLP1Emoticon.cli:main',
        ],
    },
)
