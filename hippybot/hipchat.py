import requests
try:
    import simplejson as json
except ImportError:
    import json

GETS = {
    'rooms': (
        'history', 'list', 'show',
    ),
    'users': (
        'list', 'show'
    ),
    'v2': (
        'room',
    )
}

POSTS = {
    'rooms': (
        'create', 'delete', 'message'
    ),
    'users': (
        'create', 'delete', 'update'
    )
}

DEFAULT_V2_NAME = 'v2'
DEFAULT_API_VERSION = '1'
DEFAULT_BASE_URL = 'https://%(api_server)s/v%(version)s/%(section)s/%(method)s'
BASE_URL_V2 = 'https://api.hipchat.com/v%(version)s/%(method)s'


class HipChatApi(object):
    """Lightweight Hipchat.com REST API wrapper
    """

    def __init__(self, auth_token, name=None, gets=GETS, posts=POSTS,
                 base_url=DEFAULT_BASE_URL, api_version=DEFAULT_API_VERSION,
                 api_server='api.hipchat.com'):
        self._auth_token = auth_token
        self._name = name
        self._gets = gets
        self._posts = posts
        self._base_url = base_url
        self._api_version = api_version
        self._api_server = api_server
        if (self._base_url is DEFAULT_BASE_URL and
                self._api_version is not DEFAULT_API_VERSION):
            self._base_url = BASE_URL_V2
            self._name = DEFAULT_V2_NAME

    def _request(self, method, params={}):
        if 'auth_token' not in params:
            params['auth_token'] = self._auth_token
        url = self._base_url % {
            'api_server': self._api_server,
            'version': self._api_version,
            'section': self._name,
            'method': method
        }
        if method in self._gets[self._name]:
            r = requests.get(url, params=params)
        elif method in self._posts[self._name]:
            r = requests.post(url, params=params)
        return json.loads(r.content)

    def __getattr__(self, attr_name):
        if self._name is None:
            return super(HipChatApi, self).__self_class__(
                auth_token=self._auth_token,
                name=attr_name
            )
        else:
            def wrapper(*args, **kwargs):
                return self._request(attr_name, *args, **kwargs)
            return wrapper
