from zope.app.component.hooks import getSite
from zope import component, interface, schema
from zope.component.globalregistry import provideUtility

from z3ext.content.type.interfaces import IContentType
from z3ext.principal.profile.interfaces import IProfileFields
from z3ext.persistent.fields import vocabulary
from z3ext.content.schema.interfaces import IContentSchema, ISchemaAware, \
                                            IContentSchemaStaticField

from z3ext.content.space.content import ContentSpace

from zweave import _


class StaticField(object):

    interface.implements(IContentSchemaStaticField)

    def __init__(self, contenttype):
        self.contenttype = contenttype
        super(StaticField, self).__init__(title=self.title, \
                                         description=self.description)
