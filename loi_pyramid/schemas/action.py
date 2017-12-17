import colander

class ActionUpdateSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
