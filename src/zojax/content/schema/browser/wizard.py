##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface
from zope.cachedescriptors.property import Lazy
from zope.component import getUtility
from zope.traversing.browser import absoluteURL

from zojax.layoutform import Fields, PageletEditForm, button
from zojax.wizard import WizardWithTabs
from zojax.wizard.step import WizardStep, WizardStepForm
from zojax.wizard.button import WizardButton
from zojax.wizard.interfaces import ISaveable, IForwardAction
from zojax.content.forms.wizardedit import EditContentWizard
from zojax.layoutform.interfaces import ISaveAction
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.content.schema.interfaces import _


class StaticFieldWizard(WizardWithTabs):

    prefix = 'staticfield.'
    id = 'static-field-wizard'

    def upperContainer(self):
        return '%s/'%absoluteURL(self.context.__parent__, self.request)


next = WizardButton(
    title = _(u'Next'),
    condition = lambda form: not form.isLastStep() \
        and not form.step.isSaveable(),
    weight = 300,
    provides = IForwardAction)


class ViewField(WizardStepForm):

    ignoreContext = True
    formFailedMessage = _(u'Test is failed.')
    formSuccessMessage = _(u'Test is successful.')

    @Lazy
    def fields(self):
        return Fields(self.context)

    def extractData(self):
        return {}, ()

    @button.buttonAndHandler(_(u'Test'), name='test')
    def handleTest(self, action):
        data, errors = super(ViewField, self).extractData()
        if errors:
            IStatusMessage(self.request).add(self.formFailedMessage, 'warning')
        else:
            IStatusMessage(self.request).add(self.formSuccessMessage)

    def isComplete(self):
        return True
