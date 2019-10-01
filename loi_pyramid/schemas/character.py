import colander


class CharacterAdminUpdate(colander.MappingSchema):
    accountId = colander.SchemaNode(colander.String())
    name = colander.SchemaNode(colander.String())
    exp = colander.SchemaNode(colander.Integer())
    area = colander.SchemaNode(colander.String())
