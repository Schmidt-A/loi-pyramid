import colander

class ActionUpdateSchema(colander.MappingSchema):
    type        = colander.SchemaNode(colander.String())
    amount      = colander.SchemaNode(colander.Integer())
    recipeId    = colander.SchemaNode(colander.Integer())
    completed   = colander.SchemaNode(colander.String())
