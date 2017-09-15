from setuptools import setup, find_packages
import os

version = '2.0.2.dev0'

tests_require = ['plone.app.testing']

setup(name='rt.purge',
      version=version,
      description="Frontend tool for collective.purgebyid (manually purge Plone documents from cache)",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone varnish purge cache',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='https://github.com/RedTurtle/rt.purge',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['rt'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=tests_require,
      ),
      install_requires=[
          'setuptools',
          'collective.purgebyid',
          'plone.cachepurging',
          'z3c.caching',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
