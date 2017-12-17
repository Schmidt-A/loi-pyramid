import colander

#Find a way to remove the stupid blueprintId since colander wants to have the same schemas for create and update
class InventoryUpdateSchema(colander.MappingSchema):
    blueprintId = colander.SchemaNode(colander.String())
    amount      = colander.SchemaNode(colander.Integer())
