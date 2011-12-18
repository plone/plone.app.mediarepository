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
