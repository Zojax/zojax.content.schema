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
from zope.component import getUtility
from zojax.layoutform import Fields, PageletDisplayForm
from zojax.content.type.interfaces import IOrder
from zojax.content.schema.interfaces import IContentSchema

_marker = object()


class ContentSchemaView(PageletDisplayForm):

    @property
    def fields(self):
        schema = self.schema
        data = schema.getSchemaData()

        fields = []
        for name, field in IOrder(schema).items():
            if data.get(name, field.missing_value) is not field.missing_value:
                fields.append(field)

        return Fields(*fields)

    def update(self):
        self.schema = IContentSchema(self.context)

        if self.schema is not None:
            super(ContentSchemaView, self).update()

    def getContent(self):
        return self.schema.getSchemaData()

    def render(self):
        if self.schema is None or not self.fields:
            return u''

        return super(ContentSchemaView, self).render()
