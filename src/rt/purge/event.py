# -*- coding: utf-8 -*-

from zope.component import getUtility, getMultiAdapter
from plone.registry.interfaces import IRegistry
from rt.purge.interfaces import ICachePurgingSettings
from rt.purge.interfaces import IPurgerLayer
from Products.CMFCore.utils import getToolByName
from plone.browserlayer.utils import registered_layers

from rt.purge.utils import isCachePurgingEnabled


def purgeContent(object, event):
    
    registry = getUtility(IRegistry)
    if IPurgerLayer in registered_layers() and isCachePurgingEnabled(registry):
        settings = registry.forInterface(ICachePurgingSettings)
        wtool = getToolByName(object, 'portal_workflow')
        #mtool = getToolByName(object, 'portal_membership')
        review_state = wtool.getInfoFor(object, 'review_state')
        if review_state in settings.review_state:
            getMultiAdapter((object, object.REQUEST), name='rt.purge')()
