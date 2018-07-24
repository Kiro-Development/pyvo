from pyvo.model.base import PivotalResource, Instantiated, fields
from pyvo.model.metadata import TimeZone
from pyvo.model.project import MembershipSummary


class Me(Instantiated, PivotalResource):

    name = fields.StringField()
    initials = fields.StringField()
    username = fields.StringField()
    time_zone = fields.EmbeddedField(TimeZone)
    api_token = fields.StringField()
    has_google_identity = fields.BoolField()
    projects = fields.ListField(MembershipSummary)
    workspace_ids = fields.ListField()
    email = fields.StringField()
    receives_in_app_notifications = fields.BoolField()


class Person(Instantiated, PivotalResource):

    name = fields.StringField(required=True)
    email = fields.StringField(required=True)
    initials = fields.StringField()
    username = fields.StringField()
    kind = fields.StringField()
