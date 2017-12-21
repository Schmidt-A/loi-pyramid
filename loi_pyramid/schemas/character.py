import colander

class CharacterOwnerSchema(colander.MappingSchema):
    accountId = colander.SchemaNode(colander.String())
    name = colander.SchemaNode(colander.String())
    exp = colander.SchemaNode(colander.Integer())
    area = colander.SchemaNode(colander.String())
