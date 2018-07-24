from pyvo.model.base import PivotalResource, Instantiated, fields, \
    OneOf, PostValidators, RequiredOnPost
from pyvo.model.metadata import TimeZone


class Project(Instantiated, PivotalResource):

    name = fields.StringField(validators=PostValidators(RequiredOnPost()))
    version = fields.IntField()
    iteration_length = fields.IntField()
    week_start_day = fields.StringField(validators=OneOf('Sunday',
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'))
    point_scale = fields.StringField()
    point_scale_is_custom = fields.BoolField()
    bugs_and_chores_are_estimatable = fields.BoolField()
    automatic_planning = fields.BoolField()
    enable_following = fields.BoolField()
    enable_tasks = fields.BoolField()
    start_date = fields.DateField()
    time_zone = fields.EmbeddedField(TimeZone)
    velocity_averaged_over = fields.IntField()
    shown_iterations_start_time = fields.DateTimeField()
    start_time = fields.DateTimeField()
    number_of_done_iterations_to_show = fields.IntField()
    has_google_domain = fields.BoolField()
    description = fields.StringField()
    profile_content = fields.StringField()
    enable_incoming_emails = fields.BoolField()
    initial_velocity = fields.IntField()
    public = fields.BoolField()
    atom_enabled = fields.BoolField()
    current_iteration_number = fields.IntField()
    current_velocity = fields.IntField()
    current_volatility = fields.FloatField()
    account_id = fields.IntField()
    accounting_type = fields.StringField(
        validators=OneOf('unbillable',
            'billable', 'overhead'))
    featured = fields.BoolField()
    story_ids = fields.ListField()
    epic_ids = fields.ListField()
    membership_ids = fields.ListField()
    label_ids = fields.ListField()
    integration_ids = fields.ListField()
    iteration_override_numbers = fields.ListField()


class MembershipSummary(Instantiated, PivotalResource):

    project_id = fields.IntField()
    project_name = fields.StringField()
    project_color = fields.StringField()
    role = fields.StringField(
        validators=OneOf('owner', 'member', 'viewer', 'inactive')
    )
    last_viewed_at = fields.DateTimeField()
