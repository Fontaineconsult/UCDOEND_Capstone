
from marshmallow import Schema, fields, ValidationError, pre_load


class AssociatedFiles(Schema):
    id = fields.Int(dump_only=True)
    source_url = fields.Str()
    date_added = fields.DateTime()
    key = fields.Str()
    file_name = fields.Str()
    sha_256_hash = fields.Str()


class AssociatedCaptions(Schema):
    id = fields.Int(dump_only=True)
    date_added = fields.DateTime()
    key = fields.Str()
    file_name = fields.Str()
    mime_type = fields.Str()


class CaptioningMediaAssignments(Schema):
    id = fields.Int(dump_only=True)
    media_id = fields.Int()
    associated_files = fields.Nested(AssociatedFiles)
    associated_captions = fields.Nested(AssociatedCaptions)
