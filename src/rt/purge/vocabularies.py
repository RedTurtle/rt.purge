# -*- coding: utf-8 -*-

from zope.interface import implements

try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    # older Plone
    from zope.app.schema.vocabulary import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from Products.CMFCore.utils import getToolByName

from rt.purge import purgerMessageFactory as _


class VerbosityChoiceVocabulary(object):
    """Vocabulary factory for choosing verbosirt of the purge action
    """
    implements(IVocabularyFactory)

    def __call__(self, context):

        terms = [SimpleTerm(u'friendly', title=_(u'Friendly messages')),
                 SimpleTerm(u'verbose', title=_(u'Verbose messages')),
                 SimpleTerm(u'quiet', title=_(u'No messages at all')),
                 ]
        return SimpleVocabulary(terms)

verbosityChoiceVocabularyFactory = VerbosityChoiceVocabulary()
