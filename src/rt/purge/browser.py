# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

class PurgeImmediately(BrowserView):
    
    def __call__(self, *args, **kwargs):

        # XXX

        self.request.response.redirect(self.context.absolute_url() + '/view')
        return ''