# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema

from rt.purge import purgerMessageFactory as _


class IPurgerLayer(Interface):
    """Marker interface for the rt.purge layer"""


class IPurgePaths(Interface):
    """ """


class ICachePurgingSettings(Interface):
    """Settings used by the purging algorithm.
    Should be installed into ``plone.registry``.
    """

    enabled = schema.Bool(
            title=u"Enable purging",
            default=True,
        )

    cachingProxies = schema.Tuple(
            title=u"Caching proxies",
            value_type=schema.URI(),
        )

    virtualHosting = schema.Bool(
            title=u"Send PURGE requests with virtual hosting paths",
            required=True,
            default=False,
        )

    domains = schema.Tuple(
            title=u"Domains",
            required=False,
            default=(),
            missing_value=(),
            value_type=schema.URI(),
        )

    verbosity = schema.Choice(
            title=u"Message verbosity level",
            required=True,
            default=u'friendly',
            vocabulary='rt.purge.vocabulary.verbosityChoiceVocabulary',
        )
