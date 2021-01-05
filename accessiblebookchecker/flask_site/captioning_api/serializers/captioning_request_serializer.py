from marshmallow import Schema, fields
from flask_site.captioning_api.serializers.captioning_media_serializer import CaptioningMediaSchemaIdOnly
from flask_site.captioning_api.serializers.requester_serializer import RequesterSchema


class CaptioningRequestSchema(Schema):

    id = fields.Int(dump_only=True)
    requester_id = fields.Int()
    requester = fields.Nested(RequesterSchema)
    media_id = fields.Int()
    media = fields.Nested(CaptioningMediaSchemaIdOnly)
    delivery_format = fields.Str()
    employee_id = fields.Str()
