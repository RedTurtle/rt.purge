# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from rt.purge import purgerMessageFactory as _
from z3c.caching.purge import Purge
from zope.event import notify


class PurgeImmediately(BrowserView):
    def __call__(self, *args, **kwargs):
        notify(Purge(self.context))
        messages = IStatusMessage(self.request)
        messages.add(_("Item purged"), type="info")
        self.request.response.redirect(self.context.absolute_url() + "/view")
