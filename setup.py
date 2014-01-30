from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='beantool',
      version=version,
      description="A beanstalkd console client.",
      long_description="""\
A beanstalkd console client.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='beanstalk beanstalkd queue',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='',
      license='GPL 2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
