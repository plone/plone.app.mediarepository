import urllib
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from ZTUtils.Zope import complex_marshal

class FakeResultSet(list):
    """A list with an actual_result_count property like the catalog's
    Lazy list.
    """

    @property
    def actual_result_count(self):
        return len(self)

def getUniqueTagsFromResults(results):
    """Find all unique tags in the catalog query results
    """
    tags = {}
    for item in results:
        subjects = item.Subject
        if subjects is not None:
            for tag in subjects:
                tags[tag] = tags.get(tag, 0) + 1
    return tags

def getSearchTagsFromResults(results):
    """Build the list of search tags. Excludes tags used by
    all search results, and sorts the results.
    """
    tags = getUniqueTagsFromResults(results)
    numResults = len(results)
    for key, count in tags.items():
        if count == numResults:
            del tags[key]
    return sorted(tags.keys())

def makeMediaRepositoryQuery(data=None, add=None, omit=None):
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
