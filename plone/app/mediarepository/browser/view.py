import urllib
from zope.publisher.browser import BrowserView

from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from ZTUtils.Zope import complex_marshal
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.app.mediarepository import MessageFactory as _

class FakeResultSet(list):

    @property
    def actual_result_count(self):
        return len(self)

class View(BrowserView):
    """Default view for the media repository

    Liberally borrowed from Products.ImageRepository
    """

    b_size = 3
    b_orphan = 0

    def getUniqueTagsFromResults(self, results):
        """Find all unique tags in the catalog query results
        """
        tags = {}
        for item in results:
            subjects = item.Subject
            if subjects is not None:
                for tag in subjects:
                    tags[tag] = tags.get(tag, 0) + 1
        return tags

    def getSearchTagsFromResults(self, results):
        """Build the list of search tags. Excludes tags used by
        all search results, and sorts the results.
        """
        tags = self.getUniqueTagsFromResults(results)
        results_len = len(results)
        for key, count in tags.items():
            if count == results_len:
                del tags[key]
        tags = tags.keys()
        tags.sort()
        return tags

    def queryMediaRepository(self, query=None, batch=False):
        """Perform a search returning media items

        Use batch=True to send batching hints to the catalog. This is more
        efficient, but it will not work with the 'no tags' query
        (query['tags']==['']), and the results will not be usable as
        a parameter to getSearchTagsFromResults().
        """

        portal_catalog = getToolByName(self.context, 'portal_catalog')
        if query is None:
            query = {}

        # Batching hints
        if batch:
            b_size = self.b_size
            orphan = self.b_orphan
            b_start = int(self.request.get('b_start', 0))

            query['b_start'] = b_start
            query['b_size'] = b_size + orphan

        # Type filter
        portal_types = portal_catalog.uniqueValuesFor('portal_type')
        portal_types = [x for x in portal_types if x != self.context.portal_type]
        query['portal_type'] = portal_types

        # Path filter
        query['path'] = '/'.join(self.context.getPhysicalPath())

        # Tag filter

        tags = self.request.get('tags', None)
        if tags is not None:
            if tags[0] == '':
                results = portal_catalog(query)
                return FakeResultSet([x for x in results if x.Subject == ()])
            else:
                query['Subject'] = {'query':tags, 'operator':'and'}
        return portal_catalog(query)

    def makeMediaRepositoryQuery(self, data=None, add=None, omit=None):
        """Build a query string suitable for querying the media repository
        """
        d = {}
        if data is not None:
            d.update(data)
        if add is not None:
            for key in add:
                if not d.has_key(key):
                    d[key] = add[key]
                else:
                    if isinstance(d[key], list):
                        d[key] = d[key] + add[key]
        if omit is not None:
            for key in omit:
                if d.has_key(key):
                    value = omit[key]
                    if not isinstance(value, list):
                        value = [value]
                    for v in value:
                        d[key] = [x for x in d[key] if x!=v]
        qlist = complex_marshal(d.items())
        for i in range(len(qlist)):
            k, m, v = qlist[i]
            qlist[i] = '%s%s=%s' % (urllib.quote(k), m, urllib.quote(str(v)))

        return '&'.join(qlist)

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