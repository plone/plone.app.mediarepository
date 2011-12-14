import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.app.mediarepository.testing import MEDIAREPOSITORY_INTEGRATION_TESTING

class MediaRepositoryTest(unittest.TestCase):

    layer = MEDIAREPOSITORY_INTEGRATION_TESTING

    def test_create_repository(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Member', 'Manager',))

        portal.invokeFactory('plone.mediarepository', 'repo')

        self.assertTrue('repo' in portal)
        self.assertEquals(portal['repo'].portal_type, 'plone.mediarepository')