# -*- coding: utf-8 -*-

# DEPRECATED - keep only to be able to switch to version 2.0

from Products.CMFCore.utils import getToolByName
from rt.purge import purgerMessageFactory as _
from zope.interface import implementer
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    # older Plone
    from zope.app.schema.vocabulary import IVocabularyFactory


@implementer(IVocabularyFactory)
class VerbosityChoiceVocabulary(object):
    """Vocabulary factory for choosing verbosirt of the purge action
    """
    def __call__(self, context):

        terms = [SimpleTerm(u'friendly', title=_(u'Friendly messages')),
                 SimpleTerm(u'verbose', title=_(u'Verbose messages')),
                 SimpleTerm(u'quiet', title=_(u'No messages at all')),
                 ]
        return SimpleVocabulary(terms)

verbosityChoiceVocabularyFactory = VerbosityChoiceVocabulary()
