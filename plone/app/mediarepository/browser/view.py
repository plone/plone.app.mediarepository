from zope.publisher.browser import BrowserView

from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.app.mediarepository import MessageFactory as _
from plone.app.mediarepository.utils import FakeResultSet
from plone.app.mediarepository.utils import getSearchTagsFromResults

class View(BrowserView):
    """Default view for the media repository

    Liberally borrowed from Products.ImageRepository
    """

    b_size = 3
    b_orphan = 0

    def getSearchTagsFromResults(self, results):
        """Build the list of search tags. Excludes tags used by
        all search results, and sorts the results.
        """
        return getSearchTagsFromResults(results)

    def queryMediaRepository(self):
        """Perform a search returning media items
        """

        query = {}
        tags = self.request.form.get('tags', None)

        portal_catalog = getToolByName(self.context, 'portal_catalog')
        portal_types = portal_catalog.uniqueValuesFor('portal_type')
        portal_types = [x for x in portal_types if x != self.context.portal_type]

        query['portal_type'] = portal_types
        query['path'] = '/'.join(self.context.getPhysicalPath())

        if 'SearchableText' in self.request.form:
            query['SearchableText'] = self.request.form['SearchableText']

        # Note: We do not use batching hints in the catalogue query here,
        # because we need the full result set anyway for
        # ``getSearchTagsFromResult()``.

        if tags is not None:
            if '__notags__' in tags:
                results = portal_catalog(query)
                return FakeResultSet([x for x in results if x.Subject == ()])
            else:
                query['Subject'] = {'query':[t for t in tags if t], 'operator':'and'}
        return portal_catalog(query)

class Bulk(View):
    """Tag batch operations
    """

    def canDelete(self):
        sm = getSecurityManager()
        return bool(sm.checkPermission('Delete objects', self.context))

    def canEdit(self, item):
        sm = getSecurityManager()
        return bool(sm.checkPermission('Modify portal content', self.context))

    def allTags(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        return sorted(portal_catalog.uniqueValuesFor('Subject'))

    def iterItems(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        if self.request.form.get('selectRest', False):
            for item in self.queryMediaRepository():
                yield item.getObject()
        else:
            paths = self.request.form.get('paths', [])
            for path in paths:
                try:
                    yield portal.restrictedTraverse(path)
                except Unauthorized:
                    # Should not happen, but no need to blow up if we get here
                    pass

    def __call__(self):

        form = self.request.form

        if 'form.button.Delete' in form:
            count = 0
            if not self.canDelete():
                raise Unauthorized()
            for item in self.iterItems():
                del item.getParentNode()[item.getId()]
                count += 1

            IStatusMessage(self.request).add(_(u"${count} item(s) deleted", mapping={'count': count}))

        elif 'form.button.Update' in form:

            addTags = set(form.get('addTags', []) + form.get('newTags', []))
            removeTags = set(form.get('removeTags', []))

            count = 0
            for item in self.iterItems():
                if self.canEdit(item):
                    try:
                        tags = set(item.Subject())
                        newTags = tags.union(addTags).difference(removeTags)
                        item.setSubject(list(newTags))
                        item.reindexObject()
                    except AttributeError:
                        continue

                    count += 1

            IStatusMessage(self.request).add(_(u"${count} item(s) updated", mapping={'count': count}))


        return self.index()
