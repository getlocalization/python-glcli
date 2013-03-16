#!/usr/bin/env python

from distutils.core import setup

from setuptools import setup

setup(name='gl',
      setup_requires=["py2app"],
      version='0.2.32',
      description='Get Localization Command-Line Interface',
      author='Get Localization',
      author_email='support@getlocalization.com',
      url='http://www.getlocalization.com',
      packages=['getlocalization', 'getlocalization.cli', 'getlocalization.api', 'getlocalization.api.files', 'getlocalization.api.client','getlocalization.api.data'],
      scripts=['gl'],
      app=['gl.py']
     )
