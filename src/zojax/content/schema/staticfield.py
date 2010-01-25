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
from zope import component, interface, schema

from zojax.content.schema.interfaces import IContentSchema, ISchemaAware, \
                                            IContentSchemaStaticField

from interfaces import _


class StaticField(object):

    interface.implements(IContentSchemaStaticField)
    
    order = 0

    def __init__(self, contenttype):
        self.contenttype = contenttype
        if 'order' in self.__params__:
            order = self.__params__.pop('order')
        else:
            order = self.order
        super(StaticField, self).__init__(**self.__params__)
        self.order = order
