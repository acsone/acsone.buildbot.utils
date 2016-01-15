# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


setup(name='acsone.buildbot.utils',
      version='1.0.0b1',
      description="A library providing some extensions to buildbot",
      long_description='\n'.join((
        open('README.rst').read(),
        #open('CHANGES.rst').read(),
    )),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing',
        ],
      keywords='',
      author='ACSONE SA/NV',
      author_email='laurent.mignon__at__acsone.eu',
      url='https://github.com/acsone/acsone.buildbot.utils',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['acsone', 'acsone.buildbot'],
      test_suite='tests',
      install_requires=[
        'buildbot'],
     tests_require = [
        'mock',
    ]
      )