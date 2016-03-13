import falcon
import unittest
from falcon import testing
from falcon_example import server

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

    def simulate_get(self, *args, **kwargs):
        kwargs['method'] = 'GET'
        return self.simulate_request(*args, **kwargs)

    def simulate_post(self, *args, **kwargs):
        kwargs['method'] = 'POST'
        return self.simulate_request(*args, **kwargs)

    def simulate_put(self, *args, **kwargs):
        kwargs['method'] = 'PUT'
        return self.simulate_request(*args, **kwargs)

    def simulate_delete(self, *args, **kwargs):
        kwargs['method'] = 'DELETE'
        return self.simulate_request(*args, **kwargs)


class TestCars(TestBase):

    def setUp(self):
        super(TestCars, self).setUp()

    def tearDown(self):
        super(TestCars, self).tearDown()

    def get_car(self):
        path = '/cars/{0}/'.format(self.cars_id)
        self.simulate_get(path)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def post_car(self):
        path = '/cars/'
        body = urlencode({
            'make': 'Jeep',
            'model': 'Wrangler',
            'year': '2004',
            'color': 'Black'
        })
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.simulate_post(path, body=body, headers=headers)
        self.cars_id = response[0]['cars_id']
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

    def put_car(self):
        path = '/cars/{0}/'.format(self.cars_id)
        body = urlencode({
            'color': 'Red'
        })
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.simulate_put(path, body=body, headers=headers)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def delete_car(self):
        path = '/cars/{0}/'.format(self.cars_id)
        self.simulate_delete(path)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def test_cars(self):
        self.post_car()
        self.get_car()
        self.put_car()
        self.delete_car()
