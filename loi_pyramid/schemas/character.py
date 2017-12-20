import colander

class CharacterViewSchema(colander.MappingSchema):
    accountId = colander.SchemaNode(colander.Integer())
    name = colander.SchemaNode(colander.String())

class CharacterUpdateSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
