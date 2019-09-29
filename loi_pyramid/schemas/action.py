import colander

class ActionAdminUpdate(colander.MappingSchema):
    amount      = colander.SchemaNode(colander.Integer())
    resref      = colander.SchemaNode(colander.String())
    blueprint    = colander.SchemaNode(colander.String())
    ingredients = colander.SchemaNode(colander.String())
    completed   = colander.SchemaNode(colander.String())
