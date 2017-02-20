#!/usr/bin/env python

from os.path import join, dirname

from setuptools import find_packages, setup

VERSION = (0, 5, 3)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

with open(join(dirname(__file__), 'README')) as f:
    long_description = f.read().strip()

with open(join(dirname(__file__), 'requirements.txt')) as f:
    reqs = f.read().split('\n')

setup(name='uber-tornado-elasticsearch', version=__versionstr__,
      description='Async elasticsearch client for tornado',
      url='https://code.uberinternal.com/diffusion/ENTOR/repository/master/',
      packages=find_packages(),
      install_requires=reqs,
      author=['Debosmit Ray', 'John O\'Connor', 'Christopher McAndrews'],
      maintainer='Trust Engineering',
      maintainer_email='trust-engineering@uber.com',
      include_package_data=True,
      long_description=long_description,
      py_modules=['tornado_elasticsearch'])
