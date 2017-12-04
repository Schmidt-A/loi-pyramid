import colander

class MemberUpdateSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
