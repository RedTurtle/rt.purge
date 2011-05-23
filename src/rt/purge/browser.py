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
            
            purger = getUtility(IPurger)
          
            for path in getPathsToPurge(self.context, self.request):
                for url in getURLsToPurge(path, settings.cachingProxies):
                    status, xcache, xerror = purger.purgeSync(url)
           
                    if status != 200: #error
                        self.context.plone_utils.addPortalMessage(_('purging_error',
                                                                    default='Error purging "${url}". Status (${status})',
                                                                    mapping={'url': url, 'status' : status}),
                                                                  'error')
                    else: 
                        self.context.plone_utils.addPortalMessage(_('url_purged',
                                                                    default=u"${url} purged.",
                                                                    mapping={'url': url}), 'info')
        else:
            self.context.plone_utils.addPortalMessage(_("Chaching not enabled. Please see the site configuration"),
                                                      'error')

        self.request.response.redirect(self.context.absolute_url())
        return ''
        
