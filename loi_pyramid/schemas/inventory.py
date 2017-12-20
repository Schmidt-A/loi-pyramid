import colander

class InventoryCreateSchema(colander.MappingSchema):
    characterId = colander.SchemaNode(colander.Integer())
    blueprintId = colander.SchemaNode(colander.String())
    amount      = colander.SchemaNode(colander.Integer())

class InventoryUpdateSchema(colander.MappingSchema):
    amount      = colander.SchemaNode(colander.Integer())
