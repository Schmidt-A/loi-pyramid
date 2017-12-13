import colander

class InventoryUpdateSchema(colander.MappingSchema):
    blueprintId = colander.SchemaNode(colander.String())
    amount = colander.SchemaNode(colander.Integer())
