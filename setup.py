#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings for podcast-app

Created on Sun Apr 18 20:04:14 2021

@author: jeremylhour
"""
from setuptools import setup, find_packages

from src import __version__


with open("requirements.txt", "r") as f:
    requirements = f.readlines()

setup(
    name = 'podcast-app',
    version = __version__,
    description = 'An app to play podcasts',
    url = 'https://github.com/jlhourENSAE/podcast-app',
    author = "Jérémy L'Hour",
    license = 'MIT License',
    packages = find_packages(),
    install_requires = [req for req in requirements if req[:2] != "# "],
    entry_points = {
        'console_scripts': [
            'podcast=src.cli:main',
        ],
    }
)