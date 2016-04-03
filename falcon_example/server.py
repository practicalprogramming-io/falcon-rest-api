import json
import datetime
import falcon
from falcon_example import database


class CarsViews:

    def __init__(self, db):
        self.db = db
        self.session = db.Session()

    def on_get(self, req, resp, **kwargs):
        cars_id = req.path.split('/')[2] or None

        if cars_id is None:
            car_data = self.session.query(self.db.Cars).all()
        else:
            car_data = [self.session.query(self.db.Cars) \
                .filter(self.db.Cars.cars_id == cars_id).first()]

        if len(car_data) == 0:
            raise falcon.HTTPNotFound(
                "Car(s) not found",
                "Request did not return any records"
            )

        resp.body = [x.as_dict() for x in car_data]
        resp.status = falcon.HTTP_200


    def on_post(self, req, resp, **kwargs):
        required_keys = ['make', 'model', 'year', 'color']

        if not all(key in req.params for key in required_keys):
            raise falcon.HTTPBadRequest(
                'Missing field(s)',
                'Please fill out all form fields'
            )

        create_car = self.db.Cars()
        for attr, value in req.params.items():
            if value:
                setattr(create_car, attr, value)

        self.session.add(create_car)
        self.session.commit()

        resp.body = create_car.as_dict()
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp, **kwargs):
        cars_id = req.path.split('/')[2] or None

        if cars_id is None:
            raise falcon.HTTPBadRequest(
                'No identifier',
                'Please supply an identifier for the car being updated'
            )

        car_data = self.session.query(self.db.Cars) \
            .filter(self.db.Cars.cars_id == cars_id).first()

        if car_data is None:
            raise falcon.HTTPNotFound(
                "Car(s) not found",
                "Request did not return any records"
            )

        for attr, value in req.params.items():
            if value:
                setattr(car_data, attr, value)
        car_data.updated = datetime.datetime.utcnow()

        self.session.commit()

        resp.status = falcon.HTTP_200
        resp.location = '/cars/{0}/'.format(car_data.cars_id)

    def on_delete(self, req, resp, **kwargs):
        cars_id = req.path.split('/')[2] or None

        if cars_id is None:
            raise falcon.HTTPBadRequest(
                'No identifier',
                'Please supply an identifier for the car being updated'
            )

        car_data = self.session.query(self.db.Cars) \
            .filter(self.db.Cars.cars_id == cars_id).first()

        if car_data is None:
            raise falcon.HTTPNotFound(
                "Car(s) not found",
                "Request did not return any records"
            )

        self.session.delete(car_data)
        self.session.commit()

        resp.status = falcon.HTTP_200


server = falcon.API()
cars_views = CarsViews(database)
server.add_route('/cars/', cars_views)
server.add_route('/cars/{cars_id}/', cars_views)
