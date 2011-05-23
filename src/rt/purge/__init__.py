# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

purgerMessageFactory =  MessageFactory('rt.purge')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
