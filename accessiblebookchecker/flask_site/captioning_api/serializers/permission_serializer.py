from marshmallow import Schema, fields, ValidationError, pre_load



class PermissionSchema(Schema):


    user_id = fields.Str(dump_only=True)
    permission_type = fields.Str()


permission_serializer = PermissionSchema(many=True)
