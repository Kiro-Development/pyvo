from pyvo.model.error import Error

from pyvo.model.person import Me
from pyvo.model.project import Project
from pyvo.model.story import Story, Epic
from pyvo.model.metadata import Label


class ModelNotFound(Exception):
    pass


def generate_resources(response, client=None):

    def generate(resource):
        kind = resource['kind']

        print(f'generating {kind}')

        resource_class = {
            'project': Project,
            'me': Me,
            'story': Story,
            'epic': Epic,
            'label': Label,
            'error': Error
        }.get(kind)

        if resource_class is None:
            raise ModelNotFound("No model found for {}".format(kind))

        return resource_class(**resource)

    response = response.json()

    if isinstance(response, list):
        return (generate(resource) for resource in response)
    else:
        return generate(response)
