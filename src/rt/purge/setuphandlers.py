# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from rt.purge import logger


def migrateTo1000(context):
    setup_tool = getToolByName(context, 'portal_setup')
    logger.info("Cleaning old configuration")
    setup_tool.runImportStepFromProfile('profile-rt.purge:to1000', 'plone.app.registry')
    # update
    setup_tool.runImportStepFromProfile('profile-rt.purge:default', 'plone.app.registry')
    setup_tool.runImportStepFromProfile('profile-rt.purge:default', 'actions')
    setup_tool.runImportStepFromProfile('profile-rt.purge:default', 'controlpanel')
    logger.info('Migrated to version 1.5')

def migrateTo2000(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-rt.purge:to2000')
    setup_tool.runImportStepFromProfile('profile-rt.purge:default', 'controlpanel')
    setup_tool.runImportStepFromProfile('profile-rt.purge:default', 'actions')
    logger.info('Migrated to version 2.0')
