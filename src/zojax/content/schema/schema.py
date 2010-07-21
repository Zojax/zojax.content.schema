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
from zope.component.interfaces import ComponentLookupError
"""

$Id$
"""
from BTrees.IOBTree import IOBTree

from zope import interface, component
from zope.component import getUtility
from zope.security.proxy import removeSecurityProxy
from zope.proxy import removeAllProxies
from zope.annotation.interfaces import IAnnotations
from zope.app.intid.interfaces import IIntIds
from zojax.controlpanel.interfaces import IConfigletData
from zojax.content.type.configlet import ContentContainerConfiglet, ItemLocationProxy
from zojax.content.type.interfaces import IContent, IContentType
from zojax.content.type.configlet import ConfigletContainerOrder

from interfaces import ISchemaAware, IContentSchema, IContentSchemaConfiglet, \
                       IContentSchemaStaticField

ANNOTATION_KEY = 'zojax.content.schema'


class ContentSchema(ContentContainerConfiglet):
    component.adapts(ISchemaAware)
    interface.implements(IContentSchema)

    context = None
    __tests__ = ()

    def __init__(self, contenttype):
        if not IContentType.providedBy(contenttype):
            self.bind(contenttype)
            contenttype = IContentType(contenttype)
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
            if IContentSchemaStaticField.providedBy(field):
                fid = hash(name)
            else:
                fid = intids.getId(field)
            data[name] = contentdata.get(fid, getattr(field, 'default', None))

        return data

    def setSchemaData(self, data):
        intids = getUtility(IIntIds)

        contentdata = self.contentdata

        changes = []

        for name, field in self.items():
            value = data.get(name, field.default)

            if IContentSchemaStaticField.providedBy(field):
                fid = hash(name)
            else:
                fid = intids.getId(field)

            if contentdata.get(fid) != value:
                changes.append(name)
                contentdata[fid] = value

        return changes

    def values(self):
        return [field for name, field in self.getStaticFields()] + list(super(ContentSchema, self).values())

    def keys(self):
        return [name for name, field in self.getStaticFields()] + list(self.data.keys())

    def items(self):
        return [(name, self[name]) for name in self]

    def get(self, key, default=None):
        item = self.data.get(key, default)

        if item is default:
            item = dict(self.getStaticFields()).get(key, default)
            if item is default:
                return item

        return ItemLocationProxy(removeAllProxies(item), self)

    def __contains__(self, key):
        return key in self.data

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, key):
        item = self.get(key)
        if item is None:
            raise KeyError(key)
        return item

    def getStaticFields(self):
        fields = []
        for name, field in component.getAdapters((self.contenttype,), IContentSchemaStaticField):
            field.__name__ = str(name)
            fields.append((field.order, name, field))
        fields.sort()
        return [(name, field) for order, name, field in fields]

    def __len__(self):
        '''See interface `IReadContainer`'''
        return super(ContentSchema, self).__len__() + len(self.getStaticFields())


class ContentSchemaOrder(ConfigletContainerOrder):

    def __init__(self, *kv, **kw):
        super(ContentSchemaOrder, self).__init__(*kv, **kw)
        if len(self.context) != len(self):
            for key in set(self.context.keys()).difference(set(self.keys())):
                self.addItem(key)
            for key in set(self.keys()).difference(set(self.context.keys())):
                self.removeItem(key)


@component.adapter(IContent)
@interface.implementer(IContentSchema)
def getContentSchema(content):
    ct = IContentType(content, None)
    if ct is not None:
        schema = IContentSchema(ct, None)
        if schema is not None:
            return schema.bind(content)
