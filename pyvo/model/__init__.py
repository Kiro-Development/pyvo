from pyvo.model.error import Error


class ModelNotFound(Exception):
    pass


def generate_resources(response, request, client=None):
    """
    from pyvo.model.person import Me
    from pyvo.model.project import Project
    from pyvo.model.story import Story, Epic
    from pyvo.model.metadata import Label

    def generate(resource):
        kind = resource['kind']

        print("generating {}".format(kind))

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
    """

    data = response.json()
    headers = response.headers

    if isinstance(data, list):
        for element in data:
            yield element

        # TODO check the math
        while limit + offset < total:
            newElements = self._grow()
            for element in newElements:
                yield element
    else:
        return data
