import urllib
from zope.publisher.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from ZTUtils.Zope import complex_marshal

class View(BrowserView):
    """Default view for the media repository

    Liberally borrowed from Products.ImageRepository
    """

    b_size = 40
    b_orphan = 0

    def getUniqueKeywordsFromResults(self, results):
        """Find all unique keywords in the catalog query results
        """
        keywords = {}
        for item in results:
            subjects = item.Subject
            if subjects is not None:
                for keyword in subjects:
                    keywords[keyword] = keywords.get(keyword, 0) + 1
        return keywords

    def getSearchKeywordsFromResults(self, results):
        """Build the list of search keywords. Excludes keywords used by
        all search results, and sorts the results.
        """
        keywords = self.getUniqueKeywordsFromResults(results)
        results_len = len(results)
        for key, count in keywords.items():
            if count == results_len:
                del keywords[key]
        keywords = keywords.keys()
        keywords.sort()
        return keywords

    def queryMediaRepository(self, query=None, batch=False):
        """Perform a search returning media items

        Use batch=True to send batching hints to the catalog. This is more
        efficient, but it will not work with the 'no keywords' query
        (query['keywords']==['']), and the results will not be usable as
        a parameter to getSearchKeywordsFromResults().
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

        # Keyword filter

        keywords = self.request.get('keywords', None)
        if keywords is not None:
            if keywords[0] == '':
                results = portal_catalog(query)
                return [x for x in results if x.Subject == ()]
            else:
                query['Subject'] = {'query':keywords, 'operator':'and'}
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

