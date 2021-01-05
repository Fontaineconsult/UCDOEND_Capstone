from marshmallow import Schema, fields, ValidationError, pre_load
from flask_site.captioning_api.serializers.ast_job_status_serializer import AstJobStatus


class AstJobSchema(Schema):


    id = fields.Int(dump_only=True)
    caption_job_id = fields.Int()
    captioning_status = fields.Str()
    ast_status = fields.Nested(AstJobStatus, many=True)
    added_date = fields.DateTime()
    ast_batch_id = fields.Str()
    ast_description = fields.Str()
    ast_basename = fields.Str()
    ast_language = fields.Str()
    ast_rush = fields.Str()
    ast_have_trans = fields.Bool()
    ast_notes = fields.Str()
    ast_persistent_note = fields.Int()
    ast_purchase_order = fields.Int()
    ast_callback = fields.Str()
    ast_status_url = fields.Str()
    ast_id = fields.Str()
    media_file_id = fields.Str()
