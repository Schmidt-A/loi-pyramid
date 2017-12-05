import colander

class ReputationUpdateSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
