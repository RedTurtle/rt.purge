from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='rt.purge',
      version=version,
      description="redturtle purger",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone varnish purge rt',
      author='redturtle team',
      author_email='andrew.mleczko@redturtle.it',
      url='http://blog.redturtle.it',
      license='GPL',
      packages = find_packages('src'),
      package_dir = {'': 'src'},      
      namespace_packages=['rt'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.interface',
          'zope.component',
          'zope.event',
          'zope.annotation',
          'zope.lifecycleevent',
          'zope.i18nmessageid',
          'plone.registry',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
