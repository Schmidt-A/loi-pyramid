import colander

class MemberUpdateSchema(colander.MappingSchema):
    role        = colander.SchemaNode(colander.String())
    active      = colander.SchemaNode(colander.Boolean())
