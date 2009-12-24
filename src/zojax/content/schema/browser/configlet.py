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
from zope import component, interface
from zope.component import getUtilitiesFor, queryUtility, queryMultiAdapter
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher
from zojax.content.type.interfaces import IContentType
from zojax.content.schema.interfaces import \
    ISchemaAware, IContentSchema, IContentSchemaConfiglet


class ConfigletView(object):

    def listContentTypes(self):
        cts = []
        for name, ct in getUtilitiesFor(ISchemaAware):
            cts.append((ct.title, ct))

        cts.sort()
        return [ct for _t, ct in cts]


class ConfigletPublisher(object):
    interface.implements(IBrowserPublisher)
    component.adapts(IContentSchemaConfiglet, interface.Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        view = queryMultiAdapter((self.context, request), name=name)
        if view is not None:
            return view

        ct = queryUtility(IContentType, name)
        if ct is not None:
            schema = IContentSchema(ct, None)
            if schema is not None:
                schema.__name__ = name
                schema.__parent__ = self.context
                return schema

        raise NotFound(self, name, request)

    def browserDefault(self, request):
        return self.context, ('index.html',)
