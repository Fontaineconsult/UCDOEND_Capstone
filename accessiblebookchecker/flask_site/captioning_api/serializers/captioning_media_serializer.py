from marshmallow import Schema, fields, ValidationError, pre_load
from flask_site.captioning_api.serializers.amara_serializer import AmaraSerializerSchema


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


class CaptionedResources(Schema):

    id = fields.Int(dump_only=True)
    media_id = fields.Int()
    amara_id = fields.Int()
    amara_resource = fields.Nested(AmaraSerializerSchema)


class CaptioningMediaSchema(Schema):

    id = fields.Int(dump_only=True)
    media_type = fields.Str()
    title = fields.Str()
    length = fields.Str()
    source_url = fields.Str()
    captioned_url = fields.Str()
    at_catalog_number = fields.Str()
    comments = fields.Str()
    date_added = fields.Str()
    sha_256_hash = fields.Str()
    media_objects = fields.Nested(CaptioningMediaAssignments, many=True)
    captioned_resources = fields.Nested(CaptionedResources, many=True)
    primary_caption_resource_id = fields.Int()


class CaptioningMediaSchemaIdOnly(Schema):

    id = fields.Int(dump_only=True)


media_serializer = CaptioningMediaSchema(many=True)