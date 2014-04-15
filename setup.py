# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os, sys
import pkg_resources

import norikraclient


long_description = open(os.path.join("README.rst")).read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Topic :: Software Development :: Testing",
    "Topic :: System :: Monitoring",
    "Topic :: System :: Systems Administration",
]

requires = ['msgpack-python', 'requests']
deplinks = []

setup(
    name='norikra-client-python',
    version=norikraclient.__version__,
    description='norikra-client-python library',
    long_description=long_description,
    classifiers=classifiers,
    keywords=['norikra', 'streaming', 'procesing'],
    author='WAKAYAMA Shirou',
    author_email='shirou.faw at gmail.com',
    url='http://github.com/shirou/norikra-client-python',
    download_url='http://pypi.python.org/pypi/norikra-client-python',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    dependency_links=deplinks
)

