import unittest2 as unittest

class MediaRepositoryUtilsTest(unittest.TestCase):

    def test_getUniqueTagsFromResults(self):
        from plone.app.mediarepository.utils import getUniqueTagsFromResults

        class FakeBrain(object):
            def __init__(self, subject):
                self.Subject = subject

        results = [
            FakeBrain(None),
            FakeBrain(None),
            FakeBrain(['one']),
            FakeBrain(['one', 'two']),
            FakeBrain(['three']),
            FakeBrain([]),
            FakeBrain(['four']),
        ]

        self.assertEqual(getUniqueTagsFromResults(results), {'four': 1, 'three': 1, 'two': 1, 'one': 2})

    def test_getUniqueTagsFromResults_empty(self):
        from plone.app.mediarepository.utils import getUniqueTagsFromResults

        class FakeBrain(object):
            def __init__(self, subject):
                self.Subject = subject

        results = []

        self.assertEqual(getUniqueTagsFromResults(results), {})

    def test_getUniqueTagsFromResults_none(self):
        from plone.app.mediarepository.utils import getUniqueTagsFromResults

        class FakeBrain(object):
            def __init__(self, subject):
                self.Subject = subject

        results = [
            FakeBrain(None),
            FakeBrain(None)
        ]

        self.assertEqual(getUniqueTagsFromResults(results), {})

    def test_getSearchTagsFromResults_different(self):
        from plone.app.mediarepository.utils import getSearchTagsFromResults

        class FakeBrain(object):
            def __init__(self, subject):
                self.Subject = subject

        results = [
            FakeBrain(None),
            FakeBrain(None),
            FakeBrain(['one']),
            FakeBrain(['one', 'two']),
            FakeBrain(['three']),
            FakeBrain([]),
            FakeBrain(['four']),
        ]

        self.assertEqual(getSearchTagsFromResults(results), ['four', 'one', 'three', 'two'])

    def test_getSearchTagsFromResults_common(self):
        from plone.app.mediarepository.utils import getSearchTagsFromResults

        class FakeBrain(object):
            def __init__(self, subject):
                self.Subject = subject

        results = [
            FakeBrain(['one']),
            FakeBrain(['one', 'two']),
            FakeBrain(['one', 'three']),
            FakeBrain(['one']),
            FakeBrain(['one', 'four']),
        ]

        self.assertEqual(getSearchTagsFromResults(results), ['four', 'three', 'two'])