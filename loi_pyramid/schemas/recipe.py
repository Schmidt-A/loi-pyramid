import colander

class RecipeAdminUpdate(colander.MappingSchema):
    name        = colander.SchemaNode(colander.String())
    category    = colander.SchemaNode(colander.String())
    actions     = colander.SchemaNode(colander.Integer())
    time        = colander.SchemaNode(colander.Integer())
    cost        = colander.SchemaNode(colander.String())
    requirement = colander.SchemaNode(colander.String())
