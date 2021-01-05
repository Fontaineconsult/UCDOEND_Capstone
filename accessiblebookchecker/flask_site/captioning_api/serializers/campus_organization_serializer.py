from marshmallow import Schema, fields


class CampusOrganizationSchema(Schema):

    id = fields.Int(dump_only=True)
    organization_name = fields.Str()
    organization_contact = fields.Str()
    organization_comments = fields.Str()
    organization_email = fields.Str()


class CampusOrganizationAssignmentSchema(Schema):

    id = fields.Int(dump_only=True)
    campus_org_id = fields.Str()
    employee_id = fields.Str()



campus_organization_serializer = CampusOrganizationSchema(many=True)
