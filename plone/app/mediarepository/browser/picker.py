from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView


class Picker(BrowserView):
    def __init__(self, context, request):
        self.context = context
        BrowserView.__init__(self, context, request)

    def getUploadUrl(self, repo):
        return '%s/@@quick_upload' % repo.absolute_url_path()

    def getDataForUploadUrl(self, repo):
        return 'data_url'

    def getRepositories(self):
        """Fetch everything of type plone.mediarepository"""
        catalog = getToolByName(self.context, 'portal_catalog')
        results = [b.getObject() for b in catalog.searchResults(portal_type='plone.mediarepository')]
        return results
