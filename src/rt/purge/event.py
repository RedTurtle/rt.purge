# -*- coding: utf-8 -*-

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from rt.purge.interfaces import ICachePurgingSettings
from rt.purge.interfaces import IPurgerLayer
from Products.CMFCore.utils import getToolByName
from AccessControl import Unauthorized
from plone.browserlayer.utils import registered_layers

from rt.purge.utils import isCachePurgingEnabled


def purgeContent(object, event):
    

    if IPurgerLayer in registered_layers():
        registry = getUtility(IRegistry)
        if isCachePurgingEnabled(registry):
            settings = registry.forInterface(ICachePurgingSettings)
            wtool = getToolByName(object, 'portal_workflow')
            #mtool = getToolByName(object, 'portal_membership')
            review_state = wtool.getInfoFor(object, 'review_state')
            if review_state in settings.review_state:
                try:
                    object.restrictedTraverse('@@rt.purge')()
                except Unauthorized:
                    pass
