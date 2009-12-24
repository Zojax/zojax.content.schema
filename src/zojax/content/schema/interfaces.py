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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.content.schema')


class ISchemaAware(interface.Interface):
    """ marker interface for content types that supports persistent schema """


class IContentSchema(interface.Interface):
    """ content schema """

    context = interface.Attribute('Bound context')

    def bind(context):
        """ bind schema to context and return schema """

    def getSchemaData():
        """ get content data """

    def setSchemaData(data):
        """ store schema data """


class IContentSchemaConfiglet(interface.Interface):
    """ configlet """

    def getSchema(contenttype):
        """ return content schema """
