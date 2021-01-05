from marshmallow import Schema, fields




class AstJobStatus(Schema):


    id = fields.Int(dump_only=True)
    added_date = fields.DateTime()
    job_id = fields.Int()
    ast_id = fields.Str()
    ast_type = fields.Str()
    ast_result = fields.Str()
    ast_status = fields.Str()
    ast_error_detail = fields.Str()

