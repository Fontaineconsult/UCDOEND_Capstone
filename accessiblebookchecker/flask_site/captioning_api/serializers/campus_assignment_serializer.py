from marshmallow import Schema, fields
import toastedmarshmallow

class CampusAssignmentSerializer(Schema):

    class Meta:
        jit = toastedmarshmallow.Jit

    id = fields.Int(dump_only=True)
    campus_org_id = fields.Int()
    employee_id = fields.Int()

serialize_campus_assignment = CampusAssignmentSerializer(many=True)
