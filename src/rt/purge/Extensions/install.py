# -*- coding: utf-8 -*-

from rt.purge import logger


def uninstall(portal, reinstall=False):
    if not reinstall:
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-rt.purge:uninstall')
        logger.info("Uninstall done")
