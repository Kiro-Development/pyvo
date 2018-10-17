import requests
import purl

from pyvo.model import generate_resources

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(levelname)s [%(asctime)s] -- %(message)s'
))
logger.addHandler(handler)
logger.setLevel(logging.WARN)

def debug(*args):
    msg = ", ".join(map(str, args))
    logger.debug(msg)


PIVOTAL_TRACKER_TOKEN = '2a2c2003c8e45a643ad8af2b066b3e71'

class NullReturnedError(Exception):
    pass

class ResourceNotFound(Exception):
    pass

HTTP_VERBS = ('head', 'options', 'get', 'post', 'put', 'patch', 'delete')

class ResponseType(object):
    RAW = "raw"
    JSON = "json"
    RESOURCE = "resource"

ResponseType.DEFAULT = ResponseType.RESOURCE

class Request(object):
    """docstring for Request"""
    def __init__(self, method=None, session=None,
            auth_callable=(lambda x: x), base_url=None,
            uriparts=None, baseparts=None, sent=False,
            client=None, queryparts=None):
        self.queryparts = queryparts or {}

        self.method = method
        self.session = session
        self.auth_callable = auth_callable
        self.base_url = base_url
        self.uriparts = uriparts or []
        self.baseparts = baseparts or []
        self.sent = sent
        self.client = client

    def augment_request(self, arg, reset=False):
        debug("augment_request", reset, arg, self.uriparts, self.baseparts)
        if reset:
            self.uriparts = self.baseparts[:]
            if arg is not None:
                self.uriparts.append(arg)
            return Request(
                method=self.method,
                session=self.session,
                auth_callable=self.auth_callable,
                base_url=self.base_url,
                uriparts=self.uriparts,
                baseparts=self.baseparts,
                sent=False
            )
        else:
            self.uriparts.append(arg)
            self.baseparts = self.uriparts
            return self

    def reset_request(self):
        self.augment_request(None, reset=True)

    def augment_queryparts(self, queryparts):
        self.queryparts.update(queryparts)

    def _send(self, method, response_type, **kwargs):

        url = purl.URL(self.base_url)
        # debug(resource_ids)
        debug("entered send", self.uriparts, self.baseparts)

        for p in self.uriparts:
            url = url.add_path_segment(p)

        for k, v in self.queryparts.items():
            url.query_param(k, v)

        print(url.query())

        request = requests.Request(method, url, **kwargs)

        if self.session is None:
            self.session = requests.Session()

        prepped = self.auth_callable(self.session.prepare_request(request))
        debug(prepped, prepped.url)

        resp = self.session.send(prepped)
        self.sent = True

        # remove post endpoint for subsequent requests
        if method == 'post':
            post_endpoint = self.uriparts.pop()

        if resp.status_code == 404:
            raise ResourceNotFound(resp.content)

        # XXX clean this up since these types don't support pagination
        if response_type == ResponseType.JSON:
            return resp.json()
        elif response_type == ResponseType.RAW:
            return resp
        else:
            data = resp.json()
            if isinstance(data, list):
                return PaginatedList(resp, self, method, response_type, **kwargs)
            else:
                return data

            # return generate_resources(resp, self, self.client)

    def __getattr__(self, k):
        try:
            return object.__getattr__(self, k)
        except AttributeError:
            return self.augment_request(k, reset=self.sent)

    def __call__(self, id=None,
            response_type=ResponseType.DEFAULT, **kwargs):
        if self.uriparts[-1] in HTTP_VERBS:
            method = self.uriparts.pop()
            if id is not None:
                self.augment_request(id)
            return self._send(method, response_type, **kwargs)
        else:
            if id is not None:
                return self.augment_request(id, reset=self.sent)
            elif self.method == 'post':
                return self.reset_request()
            else:
                return self


class Client(object):
    def __init__(self, token,
            base_url='https://www.pivotaltracker.com/services/v5/'):
        self.token = token
        self.base_url = base_url
        self.session = requests.Session()

    def token_auth(self, request):
        request.headers.update({
            'x-trackertoken': self.token
        })
        return request

    def request(self, **kwargs):
        return Request(session=self.session, auth_callable=self.token_auth,
            base_url=self.base_url, client=self, **kwargs)

    def __getattr__(self, k):
        try:
            return object.__getattr__(self, k)
        except AttributeError:
            request = self.request(uriparts=[k])
            return request
