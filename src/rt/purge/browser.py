from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from rt.purge.interfaces import IPurger, ICachePurgingSettings
from rt.purge.utils import getURLsToPurge, isCachePurgingEnabled, getPathsToPurge

class PurgeImmediately(object):
    """Purge immediately
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self):
        
        if isCachePurgingEnabled():
            
            registry = getUtility(IRegistry)
            settings = registry.forInterface(ICachePurgingSettings)
            
            purger = getUtility(IPurger)
          
            for path in getPathsToPurge(self.context, self.request):
                for url in getURLsToPurge(path, settings.cachingProxies):
                    status, xcache, xerror = purger.purgeSync(url)
           
                    if status != 200: #error
                        self.context.plone_utils.addPortalMessage('Error purging "%s". Status (%s)' % (url, status), 'error')
                    else: 
                        self.context.plone_utils.addPortalMessage("%s purged." % url, 'info')
        else:
            self.context.plone_utils.addPortalMessage("Chaching not enabled.\nPlease see the site configuration",
                                                      'error')

        self.request.response.redirect(self.context.absolute_url())
        return ''
        
