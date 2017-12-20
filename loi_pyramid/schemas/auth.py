import colander

class LoginSchema(colander.MappingSchema):
    user = colander.SchemaNode(colander.String())
    pw = colander.SchemaNode(colander.String())
