from Products.Five import BrowserView


class Picker(BrowserView):
    def __init__(self, context, request):
        self.context = context
        BrowserView.__init__(self, context, request)

    def getUploadUrl(self):
        folder_url = self.context['media-repository'].absolute_url()
        return '%s/@@quick_upload' % folder_url

    def getDataForUploadUrl(self):
        return 'data_url'
