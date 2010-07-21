##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
from zope import interface, event
from zope.lifecycleevent import ObjectModifiedEvent, Attributes
from zojax.layoutform import Fields, PageletEditSubForm
from zojax.content.type.interfaces import IOrder
from zojax.content.schema.interfaces import _, IContentSchema
from zojax.content.schema.schema import getContentSchema


class ContentSchemaEdit(PageletEditSubForm):

    schema = None
    prefix = 'content.schema'
    label = _('Custom fields')

    @property
    def fields(self):
        return Fields(*list(IOrder(self.schema).values()))

    def getContent(self):
        return self.schema.getSchemaData()

    def update(self):
        schema = IContentSchema(self.context, None)

        if schema is not None and schema.context is not None:
            self.schema = schema
            super(ContentSchemaEdit, self).update()

    def isAvailable(self):
        return self.schema is not None and len(self.schema)

    def applyChanges(self, data):
        changes = self.schema.setSchemaData(data)
        if changes:
            event.notify(ObjectModifiedEvent(self.context, Attributes(IContentSchema, *changes)))
            return {IContentSchema: changes}
        else:
            return {}
