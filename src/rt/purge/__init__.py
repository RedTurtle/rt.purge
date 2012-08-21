# -*- coding: utf-8 -*-

import logging

from zope.i18nmessageid import MessageFactory

purgerMessageFactory =  MessageFactory('rt.purge')
logger = logging.getLogger('rt.purge')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
