import colander

class RecipeUpdateSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
