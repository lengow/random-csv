#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='random_csv',
    version='1.0.0',
    author='Lucie Masson',
    author_email='lucie.masson@lengow.com',
    packages=['random_csv'],
    url='https://github.com/lengow/random-csv',
    license='LICENSE.txt',
    description='Generate a random csv file',
    long_description=open('README.md').read(),
    install_requires=['namealizer'],
)