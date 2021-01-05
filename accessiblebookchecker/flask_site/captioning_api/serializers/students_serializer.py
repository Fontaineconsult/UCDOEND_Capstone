from marshmallow import Schema, fields, ValidationError, pre_load


class StudentsSchema(Schema):

    id = fields.Int(dump_only=True)
    student_id = fields.Str()
    student_first_name = fields.Str()
    student_last_name = fields.Str()
    student_email = fields.Str()
    student_requests = fields.Str()
    captioning_active = fields.Boolean()
    transcripts_only = fields.Boolean()


students_query_serializer = StudentsSchema(many=True)