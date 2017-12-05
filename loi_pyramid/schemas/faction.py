import colander

class FactionUpdateSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
