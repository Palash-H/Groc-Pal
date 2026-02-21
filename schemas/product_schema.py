from marshmallow import Schema, fields, validate


class ProductCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2))
    category_id = fields.Integer(required=True)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)
    man_date = fields.Date(required=True)


class ProductUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=2))
    category_id = fields.Integer()
    price = fields.Float()
    quantity = fields.Integer()
    man_date = fields.Date()


class ProductResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    category_id = fields.Integer()
    price = fields.Float()
    quantity = fields.Integer()
    man_date = fields.Date()