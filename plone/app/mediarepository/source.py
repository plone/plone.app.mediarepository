from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName

from plone.formwidget.contenttree import UUIDSourceBinder

from plone.app.mediarepository.interfaces import IMediaRepository

class MediaRepoSourceBinder(UUIDSourceBinder):

    def __call__(self, context):
        site = getSite()
        catalog = getToolByName(site, 'portal_catalog')
        
        repos = catalog({'object_provides': IMediaRepository.__identifier__})
        paths = [p.getPath() for p in repos]

        self.navigation_tree_query = {'path': {'query': paths}}
        source = super(MediaRepoSourceBinder, self).__call__(context)
        return source
