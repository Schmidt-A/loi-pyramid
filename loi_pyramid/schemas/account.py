import colander

class AccountViewSchema(colander.MappingSchema):
    role        = colander.SchemaNode(colander.Integer())
    approved    = colander.SchemaNode(colander.Integer())
    banned      = colander.SchemaNode(colander.Integer())

class AccountUpdateSchema(colander.MappingSchema):
    role        = colander.SchemaNode(colander.Integer())
    approved    = colander.SchemaNode(colander.Integer())

class AccountInternalUpdateSchema(colander.MappingSchema):
    cdkey       = colander.SchemaNode(colander.String())
    role        = colander.SchemaNode(colander.Integer())
    approved    = colander.SchemaNode(colander.Integer())
    banned      = colander.SchemaNode(colander.Integer())
