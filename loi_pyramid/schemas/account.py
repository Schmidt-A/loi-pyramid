import colander

class AccountOwnerUpdate(colander.MappingSchema):
    approved    = colander.SchemaNode(colander.Integer())

class AccountAdminUpdate(colander.MappingSchema):
    cdkey       = colander.SchemaNode(colander.String())
    role        = colander.SchemaNode(colander.Integer())
    approved    = colander.SchemaNode(colander.Integer())
    banned      = colander.SchemaNode(colander.Integer())
