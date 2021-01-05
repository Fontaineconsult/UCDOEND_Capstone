from marshmallow import Schema, fields
from flask_site.captioning_api.serializers.courses_serializer import CoursesSchema
from flask_site.captioning_api.serializers.captioning_media_serializer import CaptioningMediaSchema
from flask_site.captioning_api.serializers.ast_job_serializer import AstJobSchema

class CaptionJobSchema(Schema):

    id = fields.Int(dump_only=True)
    requester_id = fields.Int()
    course_id = fields.Str()
    course = fields.Nested(CoursesSchema)
    request_date = fields.DateTime()
    show_date = fields.DateTime()
    delivered_date = fields.DateTime()
    media_id = fields.DateTime()
    media = fields.Nested(CaptioningMediaSchema)
    output_format = fields.Str()
    comments = fields.Str()
    delivery_location = fields.Str()
    transcripts_only = fields.Boolean()
    job_status = fields.Str()
    captioning_provider = fields.Str()
    priority = fields.Boolean()
    rush_service_used = fields.Boolean()
    request_method = fields.Str()
    content_hidden = fields.Boolean()
    ast_jobs = fields.Nested(AstJobSchema, many=True)


caption_job_serializer = CaptionJobSchema(many=True)