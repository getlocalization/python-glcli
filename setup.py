#!/usr/bin/env python

from distutils.core import setup

from setuptools import setup
import sys

setup(name='gl',
      #setup_requires=["py2app"],
      version='0.2.36',
      description='Get Localization Command-Line Interface',
      author='Get Localization',
      author_email='support@getlocalization.com',
      url='http://www.getlocalization.com',
      packages=['getlocalization', 'getlocalization.cli', 'getlocalization.api', 'getlocalization.api.files', 'getlocalization.api.client','getlocalization.api.data'],
      scripts=['gl'],
      #app=['gl.py']
     )

if sys.platform == 'darwin':
    extra_options = dict(setup_requires=["py2app"],app=['gl.py'],options=dict(py2app=dict(argv_emulation=True)))
elif sys.platform == 'win32':
    extra_options = dict(setup_requires=['py2exe'],app=['gl.py'],)
