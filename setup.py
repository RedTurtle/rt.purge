from setuptools import setup, find_packages
import os

version = '1.1.0'

setup(name='rt.purge',
      version=version,
      description="Product for Plone for invalidate (purge) a page cached in Varnish",
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
      url='http://www.redturtle.it',
      license='GPL',
      packages = find_packages('src'),
      package_dir = {'': 'src'},      
      namespace_packages=['rt'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone<4.0dev',
          'zope.interface',
          'zope.component',
          'zope.event',
          'zope.annotation',
          'zope.lifecycleevent',
          'zope.i18nmessageid',
          'plone.app.registry',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
