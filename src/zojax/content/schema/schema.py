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
from BTrees.IOBTree import IOBTree

from zope import interface, component
from zope.component import getUtility
from zope.security.proxy import removeSecurityProxy
from zope.annotation.interfaces import IAnnotations
from zope.app.intid.interfaces import IIntIds
from zojax.controlpanel.interfaces import IConfigletData
from zojax.content.type.configlet import ContentContainerConfiglet
from zojax.content.type.interfaces import IContent, IContentType

from interfaces import ISchemaAware, IContentSchema, IContentSchemaConfiglet

ANNOTATION_KEY = 'zojax.content.schema'


class ContentSchema(ContentContainerConfiglet):
    component.adapts(ISchemaAware)
    interface.implements(IContentSchema)

    context = None
    __tests__ = ()

    def __init__(self, contenttype):
        self.__id__ = u'content.schema.%s'%contenttype.name
        self.__name__ = contenttype.name

        self.contenttype = contenttype

    def bind(self, context):
        self.context = context
        return self

    @property
    def title(self):
        return self.contenttype.title

    @property
    def description(self):
        return self.contenttype.description

    @property
    def contentdata(self):
        annotations = IAnnotations(removeSecurityProxy(self.context))

        data = annotations.get(ANNOTATION_KEY)
        if data is None:
            data = IOBTree()
            annotations[ANNOTATION_KEY] = data

        return data

    def getSchemaData(self):
        intids = getUtility(IIntIds)

        contentdata = self.contentdata

        data = {}
        for name, field in self.items():
            id = intids.getId(field)

            data[name] = contentdata.get(id, getattr(field, 'default', None))

        return data

    def setSchemaData(self, data):
        intids = getUtility(IIntIds)

        contentdata = self.contentdata

        changes = []

        for name, field in self.items():
            id = intids.getId(field)
            value = data.get(name, field.default)

            if contentdata.get(id) != value:
                changes.append(name)

            contentdata[id] = value

        return changes

    def values(self):
        return super(ContentSchema, self).values() + []


    def getStaticFields(self):
        return get

@component.adapter(IContent)
@interface.implementer(IContentSchema)
def getContentSchema(content):
    ct = IContentType(content, None)
    if ct is not None:
        schema = IContentSchema(ct, None)
        if schema is not None:
            return schema.bind(content)
