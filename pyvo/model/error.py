from pyvo.model.base import PivotalResource, Instantiated, fields, \
    OneOf, PostValidators, RequiredOnPost
from pyvo.model.metadata import TimeZone, Label


class PivotalValidationError(PivotalResource):
    field = fields.StringField()
    problem = fields.StringField()


class Error(PivotalResource):
    kind = fields.StringField()
    code = fields.StringField()
    error = fields.StringField()
    requirement = fields.StringField()
    general_problem = fields.StringField()
    possible_fix = fields.StringField()
    validation_errors = fields.ListField(PivotalValidationError)

    def __str__(self):
        return "{}".format(self.general_problem or self.error)
