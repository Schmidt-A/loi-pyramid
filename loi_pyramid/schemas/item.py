import colander


class ItemAdminCreate(colander.MappingSchema):
    resref = colander.SchemaNode(colander.String())
    amount = colander.SchemaNode(colander.Integer())


class ItemAdminUpdate(colander.MappingSchema):
    amount = colander.SchemaNode(colander.Integer())
