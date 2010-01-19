from zope.app.component.hooks import getSite
from zope import component, interface, schema
from zope.component.globalregistry import provideUtility

from zojax.content.type.interfaces import IContentType
from zojax.principal.profile.interfaces import IProfileFields
from zojax.persistent.fields import vocabulary
from zojax.content.schema.interfaces import IContentSchema, ISchemaAware, \
                                            IContentSchemaStaticField

from zojax.content.space.content import ContentSpace

from zweave import _


class StaticField(object):

    interface.implements(IContentSchemaStaticField)

    def __init__(self, contenttype):
        self.contenttype = contenttype
        super(StaticField, self).__init__(title=self.title, \
                                         description=self.description)
