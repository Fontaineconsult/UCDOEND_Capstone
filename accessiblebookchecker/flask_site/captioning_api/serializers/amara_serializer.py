from marshmallow import Schema, fields


class AmaraSerializerSchema(Schema):

    id = fields.Int(dump_only=True)
    url = fields.String()
    title = fields.Str()
    video_id = fields.Str()
    captions_uploaded = fields.Boolean()
    captions_complete = fields.Boolean()

