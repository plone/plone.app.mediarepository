from zope.interface import implements
from plone.dexterity.content import Container
from collective.quickupload.browser.interfaces import IQuickUploadCapable

class MediaRepository(Container):
    implements(IQuickUploadCapable)
