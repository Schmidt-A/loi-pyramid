import colander

class ItemCreateSchema(colander.MappingSchema):
    characterId = colander.SchemaNode(colander.Integer())
    blueprintId = colander.SchemaNode(colander.String())
    amount      = colander.SchemaNode(colander.Integer())

class ItemUpdateSchema(colander.MappingSchema):
    amount      = colander.SchemaNode(colander.Integer())
