import pytest
import json
import requests

from pyvo.client import Client, ResponseType, ResourceNotFound

'''
describe the Pyvo client
    it returns valid responses
    it can return json
    it can return the underlying Requests response
    it maps attributes to URL segments
    it raises an exception for 404s
    it returns a resource key with a successful response
    it produces standalone instances
    --TODO--
    it reads an API token from the environment
    it helps implementers manage oauth
'''


class TestClient():

    @pytest.fixture
    def client(self):
        return Client('2a2c2003c8e45a643ad8af2b066b3e71',
                      'https://www.pivotaltracker.com/services/v5/')

    def test_pagination(self, client):
        items = client.projects('1877193').activity.get(response_type=ResponseType.PAGINATED)
        all = list(items)

        # assert r1.status_code == 200
        assert len(all) > 100, len(all)

    def test_returns_valid_responses(self, client):
        r1 = client.me.get(response_type=ResponseType.RAW)
        r2 = client.projects.get(response_type=ResponseType.RAW)

        assert r1.status_code == r2.status_code == 200

    def test_can_return_json(self, client):
        r1 = client.me.get(response_type=ResponseType.JSON)
        assert json.dumps(r1)

    def test_maps_attributes_to_url_segments(self, client):
        r1 = client.projects(id='1040058').get(response_type=ResponseType.JSON)
        assert r1['kind'] == 'project'

        r2 = client.projects.labels(project_id='1040058', label_id='81231')
        assert r2

    def test_raises_an_exception_for_404s(self, client):
        with pytest.raises(ResourceNotFound):
            r1 = client.zod.get(response_type=ResponseType.JSON)

    def test_produces_standalone_instances(self, client):
        project = client.projects(id='1040058')

        project_json = project.get(response_type=ResponseType.RAW)
        assert project_json.status_code == 200

        labels = project.labels.get(response_type=ResponseType.RAW)
        assert labels.status_code == 200

    def test_produces_resource_entities(self, client):
        from pyvo.model.project import Project
        from pyvo.model.metadata import Label
        from pyvo.model.story import Story

        project = client.projects(id='1040058')

        p = project.get()
        assert isinstance(p, Project)

        labels = project.labels.get()
        for label in labels:
            assert isinstance(label, Label)
            assert label.project_id == 1040058

        stories = project.stories.get()
        for story in stories:
            assert isinstance(story, Story)
            assert story.story_type in ('feature', 'bug', 'chore', 'release')
