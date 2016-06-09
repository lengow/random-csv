#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='randow_csv_catalog',
    version='1.0.0',
    author='Lucie Masson',
    author_email='lucie.masson@lengow.com',
    packages=['randow_csv'],
    url='https://github.com/lengow/random-csv',
    license='LICENSE.txt',
    description='Generate a randow csv catalog',
    long_description=open('README.md').read(),
    install_requires=['namealizer'],
)