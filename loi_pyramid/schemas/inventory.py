import colander

class InventoryUpdateSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
