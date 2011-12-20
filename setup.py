from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='plone.app.mediarepository',
      version=version,
      description="Media repository using dexterity and deco",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.quickupload > 1.3.0',
          'plone.app.dexterity',
          'plone.app.contentlisting',
          'plone.namedfile [blobs]',
      ],
      extras_require={
          'test': [
            'unittest2',
            'plone.app.testing', ]},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
