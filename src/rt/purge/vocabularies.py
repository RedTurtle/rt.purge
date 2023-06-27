# -*- coding: utf-8 -*-

# DEPRECATED - keep only to be able to switch to version 2.0

from Products.CMFCore.utils import getToolByName
from rt.purge import purgerMessageFactory as _
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    # older Plone
    from zope.app.schema.vocabulary import IVocabularyFactory


class VerbosityChoiceVocabulary(object):
    """Vocabulary factory for choosing verbosirt of the purge action"""

    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = [
            SimpleTerm("friendly", title=_("Friendly messages")),
            SimpleTerm("verbose", title=_("Verbose messages")),
            SimpleTerm("quiet", title=_("No messages at all")),
        ]
        return SimpleVocabulary(terms)


verbosityChoiceVocabularyFactory = VerbosityChoiceVocabulary()
