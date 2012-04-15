#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import kaggregate

setup(
    name = 'django-kaggregate',
    version = ":versiontools:version:",
    description = "Generic aggregated data generation and store",
    long_description = "",
    keywords = 'django, model',
    author = 'Jesús Espino García',
    author_email = 'jespinog@gmail.com',
    url = 'https://github.com/kaleidos/django-kaggregate',
    license = 'BSD',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[
        'distribute',
    ],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
