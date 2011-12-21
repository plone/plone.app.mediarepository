Introduction
============

This package provides a folder type that can be used to store media assets for
a Plone site. Images, videos and other media items can be stored in large
numbers, browsed by tags, and uploaded and tagged in batch.

Installation
============

To install, you must have a Dexterity Known Good Set enabled in your buildout.
For example::

    [buildout]
    extends =
        http://good-py.appspot.com/release/dexterity/1.1?plone=4.1.3

You can then add ``plone.mediarepository`` to your ``eggs`` list or as a
dependency of another package in the ``install_requires`` list in ``setup.py``.

Usage
=====

As a ``Manager`` user, add a ``Media repository`` anywhere in the site. Use
the ``Bulk operations`` tab to upload files in bulk (best supported in modern,
HTML 5-captable browsers like Chrome and Firefox).
