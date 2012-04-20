from zope.component import getUtility
import unittest2 as unittest

from Products.TinyMCE.interfaces.utility import ITinyMCE
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.app.mediarepository.testing import \
    MEDIAREPOSITORY_INTEGRATION_TESTING


class MediaRepositoryTest(unittest.TestCase):

    layer = MEDIAREPOSITORY_INTEGRATION_TESTING

    def test_mediarepository_is_linkable_in_tinymce(self):
        utility = getUtility(ITinyMCE)
        linkable_portal_types = utility.linkable.split('\n')
        self.assertTrue('plone.mediarepository' in linkable_portal_types)

    def test_create_repository(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Member', 'Manager',))

        portal.invokeFactory('plone.mediarepository', 'repo')

        self.assertTrue('repo' in portal)
        self.assertEquals(portal['repo'].portal_type,
            'plone.mediarepository')
