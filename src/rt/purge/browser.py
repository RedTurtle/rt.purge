# -*- coding: utf-8 -*-

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from rt.purge.interfaces import IPurger, ICachePurgingSettings
from rt.purge.utils import getURLsToPurge, isCachePurgingEnabled, getPathsToPurge

from Products.Five.browser import BrowserView
from rt.purge import purgerMessageFactory as _

class PurgeImmediately(BrowserView):
    """Purge immediately
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self, *args, **kwargs):
        
        if isCachePurgingEnabled():
            
            registry = getUtility(IRegistry)
            settings = registry.forInterface(ICachePurgingSettings)
            friendly_messages = settings.friendly_messages
            
            purger = getUtility(IPurger)

            purgeCounter = 0
            for path in set(getPathsToPurge(self.context, self.request)):
                for url in getURLsToPurge(path, settings.cachingProxies):
                    status, xcache, xerror = purger.purgeSync(url)
           
                    if status != 200: #error
                        if not friendly_messages:
                            self.context.plone_utils.addPortalMessage(_('purging_error',
                                                                        default='Error purging "${url}". Status (${status})',
                                                                        mapping={'url': url, 'status' : status}),
                                                                      'warning')
                    else: 
                        if not friendly_messages:
                            self.context.plone_utils.addPortalMessage(_('url_purged',
                                                                        default=u"${url} purged.",
                                                                        mapping={'url': url}), 'info')
                        purgeCounter+=1

            if friendly_messages:
                if purgeCounter==0:
                    self.context.plone_utils.addPortalMessage(_('purging_friendly_error',
                                                                default='Unable to purge "${url}".',
                                                                mapping={'url': self.context.absolute_url(), }),
                                                              'warning')
                else:
                    self.context.plone_utils.addPortalMessage(_('url_purged',
                                                                default=u"${url} purged.",
                                                                mapping={'url': self.context.absolute_url()}), 'info')
        else:
            self.context.plone_utils.addPortalMessage(_("Chaching not enabled. Please see the site configuration"),
                                                      'error')

        self.request.response.redirect(self.context.absolute_url()+'/view')
        return ''
        
