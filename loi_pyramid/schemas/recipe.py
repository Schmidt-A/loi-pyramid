import colander

class RecipeUpdateSchema(colander.MappingSchema):
    actions     = colander.SchemaNode(colander.Integer())
    time        = colander.SchemaNode(colander.Integer())
    cost        = colander.SchemaNode(colander.String())
    requirement = colander.SchemaNode(colander.String())
