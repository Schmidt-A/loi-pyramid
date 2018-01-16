import colander

class IngredientAdminUpdate(colander.MappingSchema):
    name                = colander.SchemaNode(colander.String())
    category            = colander.SchemaNode(colander.String())
    tier                = colander.SchemaNode(colander.Integer())
    melee_stats         = colander.SchemaNode(colander.String())
    half_melee_stats    = colander.SchemaNode(colander.String())
    armor_stats         = colander.SchemaNode(colander.String())
    half_armor_stats    = colander.SchemaNode(colander.String())
