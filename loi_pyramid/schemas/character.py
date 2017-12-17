import colander

class CharacterUpdateSchema(colander.MappingSchema):
    name        = colander.SchemaNode(colander.String())
