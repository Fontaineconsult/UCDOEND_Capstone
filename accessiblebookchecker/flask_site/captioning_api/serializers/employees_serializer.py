from marshmallow import Schema, fields, ValidationError, pre_load



class EmployeeSchema(Schema):

    id = fields.Int(dump_only=True)
    employee_id = fields.Str()
    employee_first_name = fields.Str()
    employee_last_name = fields.Str()
    employee_email = fields.Str()
    employee_phone = fields.Str()
    permission_type = fields.Str()



instructor_query_serializer = EmployeeSchema()
instructors_query_serializer = EmployeeSchema(many=True)