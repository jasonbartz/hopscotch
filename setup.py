#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='hopscotch',
    version='0.0.1',
    description='A lightweight, pip-installable app that tracks alcohol drinking and collecting for the aficionado.',
    author='Jason Bartz',
    author_email='jason@jasonbartz.com',
    url='http://hopscotchapp.com',
    long_description=open('README.md', 'r').read(),
    packages=[
        'hopscotch',
        'hopscotch.dram'
    ],
    package_data={
        'hopscotch': ['templates/hopscotch/*'],
    },
    # requires=[
    #         'mimeparse',
    #         'python_dateutil(>=1.5, < 2.0)',
    #     ],
    #     install_requires=[
    #         'mimeparse',
    #         'python_dateutil >= 1.5, < 2.0',
    #     ],
)