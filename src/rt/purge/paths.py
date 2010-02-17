from zope.interface import implements
from zope.component import adapts
from rt.purge.interfaces import IPurgePaths
from OFS.interfaces import ITraversable

class TraversablePurgePaths(object):
    """Default purge for OFS.Traversable-style objects
    """
    
    implements(IPurgePaths)
    adapts(ITraversable)
    
    def __init__(self, context):
        self.context = context
        
    def getRelativePaths(self):
        paths = []
        if self.context.plone_utils.isDefaultPage(self.context):
            paths.append(self.context.aq_inner.aq_parent.absolute_url_path())
        paths.append(self.context.absolute_url_path())
        return paths
    
    def getAbsolutePaths(self):
        return []
