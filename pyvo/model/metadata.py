from pyvo.model.base import PivotalResource, Instantiated, fields


class TimeZone(PivotalResource):
    olson_name = fields.StringField()
    offset = fields.StringField()
    kind = fields.StringField()


class Label(Instantiated, PivotalResource):
    project_id = fields.IntField()
    name = fields.StringField(required=True)
