import pytest
import json
import requests

'''
describe the Pyvo client
    it returns valid responses
    it can return json
    it can return the underlying Requests response
    it maps attributes to URL segments
    it raises an exception for 404s
    --TODO--
    it reads an API token from the environment
    it helps implementers manage oauth
'''

def describe_the_pyvo_client():

    @pytest.fixture
    def client():
        from pyvo import Client
        return Client('2a2c2003c8e45a643ad8af2b066b3e71',
            'https://www.pivotaltracker.com/services/v5/')

    def it_returns_valid_responses(client):
        r1 = client.me.get(return_json=False)
        r2 = client.projects.get(return_json=False)

        assert r1.status_code == r2.status_code == 200

    def it_can_return_json(client):
        r1 = client.me.get()
        assert json.dumps(r1)

    def it_maps_attributes_to_url_segments(client):
        r1 = client.projects(id='1040058').get()
        assert r1['kind'] == 'project'

        r2 = client.projects.labels(project_id='1040058', label_id='81231')
        assert r2

    def it_raises_an_exception_for_404s(client):
        pass
