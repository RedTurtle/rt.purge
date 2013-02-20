# -*- coding: utf-8 -*-

#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from z3c.form import button

from plone.app.registry.browser import controlpanel

from rt.purge import purgerMessageFactory as _
from rt.purge.interfaces import ICachePurgingSettings


class RTPurgeSettingsControlPanelEditForm(controlpanel.RegistryEditForm):
    """rt.purge settings form.
    """
    schema = ICachePurgingSettings
    id = "RTPurgeSettingsEditForm"
    label = _(u"Purge settings")
    description = _(u"help_rtpurge_settings_editform",
                    default=u"Manage general site configuration for rt.purge")

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@rtpurge-settings")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


class RTPurgeSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """rt.purge settings control panel.
    """
    form = RTPurgeSettingsControlPanelEditForm
    #index = ViewPageTemplateFile('controlpanel.pt')
