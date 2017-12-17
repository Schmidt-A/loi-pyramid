import colander

class ReputationUpdateSchema(colander.MappingSchema):
    amount      = colander.SchemaNode(colander.Integer())
