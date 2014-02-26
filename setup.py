from setuptools import setup, find_packages

version = '0.2.13'

setup(name='beantool',
      version=version,
      description="A beanstalkd console client.",
      long_description="""\
A beanstalkd console client.""",
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
      ],
      keywords='beanstalk beanstalkd queue',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/BeanTool',
      license='GPL 2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'PyYAML==3.10',
            'beanstalkc==0.3.0',
            'phpserialize==1.3'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      scripts=['scripts/bt']
      )
