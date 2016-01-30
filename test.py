import falcon
import unittest
import json
from falcon import testing

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestBase(unittest.TestCase):

    def setUp(self):
        self.app = server.server
        self.srmock = falcon.testing.StartResponseMock()

    def simulate_request(self, path, **kwargs):
        env = falcon.testing.create_environ(path=path, **kwargs)
        return self.app(env, self.srmock)

    def simulate_head(self, *args, **kwargs):
        kwargs['method'] = 'HEAD'
        return self.simulate_request(*args, **kwargs)

    def simulate_get(self, *args, **kwargs):
        kwargs['method'] = 'GET'
        return self.simulate_request(*args, **kwargs)

    def simulate_post(self, *args, **kwargs):
        kwargs['method'] = 'POST'
        return self.simulate_request(*args, **kwargs)

    def simulate_put(self, *args, **kwargs):
        kwargs['method'] = 'PUT'
        return self.simulate_request(*args, **kwargs)

    def simulate_patch(self, *args, **kwargs):
        kwargs['method'] = 'PATCH'
        return self.simulate_request(*args, **kwargs)

    def simulate_delete(self, *args, **kwargs):
        kwargs['method'] = 'DELETE'
        return self.simulate_request(*args, **kwargs)


class TestUser(TestBase):

    def setUp(self):
        super(TestRegister, self).setUp()
        self.entry_path = '/register/'

    def tearDown(self):
        super(TestRegister, self).tearDown()

    def test_register_user(self):
        body = urlencode({
            'username': 'new_user',
            'email': 'email',
            'password': 'password',
            'location': 'Tucson, AZ'
        })
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.simulate_post(self.entry_path, body=body, headers=headers)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
