from StringIO import StringIO
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
        
        if not isCachePurgingEnabled():
            return 'Caching not enabled'
        
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICachePurgingSettings)
        
        purger = getUtility(IPurger)
        
        out = StringIO()
        
        for path in getPathsToPurge(self.context, self.request):
            for url in getURLsToPurge(path, settings.cachingProxies):
                status, xcache, xerror = purger.purgeSync(url)
                print >>out, "Purged", url, "Status", status, "X-Cache", xcache, "Error:", xerror
                print "Purged", url, "Status", status, "X-Cache", xcache, "Error:", xerror
        
        return out.getvalue()
