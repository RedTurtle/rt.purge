# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema
from rt.purge import purgerMessageFactory as _


class IPurgerLayer(Interface):
    """Marker interface for the rt.purge layer"""


class IPurgePaths(Interface):
    """ """


class ICachePurgingSettings(Interface):
    # DEPRECATED - keep only to be able to switch to version 2.0

    enabled = schema.Bool(
        title="Enable purging",
        default=True,
    )

    cachingProxies = schema.Tuple(
        title="Caching proxies",
        value_type=schema.URI(),
    )

    virtualHosting = schema.Bool(
        title="Send PURGE requests with virtual hosting paths",
        required=True,
        default=False,
    )

    domains = schema.Tuple(
        title="Domains",
        required=False,
        default=(),
        missing_value=(),
        value_type=schema.URI(),
    )

    verbosity = schema.Choice(
        title="Message verbosity level",
        required=True,
        default="friendly",
        vocabulary="rt.purge.vocabulary.verbosityChoiceVocabulary",
    )
