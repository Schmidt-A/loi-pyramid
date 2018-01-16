import colander

class ItemAdminCreate(colander.MappingSchema):
    characterId = colander.SchemaNode(colander.Integer())
    resref      = colander.SchemaNode(colander.String())
    amount      = colander.SchemaNode(colander.Integer())

class ItemAdminUpdate(colander.MappingSchema):
    amount      = colander.SchemaNode(colander.Integer())
