from marshmallow import Schema, fields
from flask_site.captioning_api.serializers.captioning_media_serializer import CaptioningMediaSchema



class iLearnVideoSchema(Schema):

    id = fields.Int(dump_only=True)
    resource_link = fields.Str()
    title = fields.Str()
    scan_date = fields.DateTime()
    video_length = fields.Str()
    captioned = fields.Boolean()
    captioned_version_id = fields.Str()
    indicated_due_date = fields.DateTime()
    submitted_for_processing = fields.Boolean()
    submitted_for_processing_date = fields.DateTime()
    course_ilearn_id = fields.Str()
    course_gen_id = fields.Str()
    semester = fields.Str()
    page_section = fields.Str()
    auto_caption_passed = fields.Boolean()
    ignore_video = fields.Boolean()
    invalid_link = fields.Boolean()

    captioned_version = fields.Nested(CaptioningMediaSchema)

ilearn_video_serializer = iLearnVideoSchema(many=True)