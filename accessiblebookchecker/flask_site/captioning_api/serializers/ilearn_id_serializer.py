from marshmallow import Schema, fields, ValidationError, pre_load

class IlearnIdSchema(Schema):

    id = fields.Int(dump_only=True)
    course_gen_id = fields.Str()
    ilearn_page_id = fields.Str()



