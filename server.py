import falcon


class User:

    def __init__(self, db):
        self.db = db

    def on_post(self, req, resp, **kwargs):
        session = self.db.Session()

        username = req.get_param('username') or None
        email = req.get_param('email') or None
        password = req.get_param('password') or None
        location = req.get_param('location') or None

        if any(x is None for x in [username, email, password, location]):
            raise falcon.HTTPBadRequest(
                'Missing field(s)',
                'Please fill out all form fields'
            )

        username_exists = session.query(self.db.Users) \
            .filter(self.db.Users.username == username)

        email_exists = session.query(self.db.Users) \
            .filter(self.db.Users.email == email)

        username_exists = session.execute(username_exists)

        if username_exists.rowcount > 0:
            raise falcon.HTTPBadRequest(
                'User is registered',
                'User with username: {0} is already registered'.format(username)
            )

        email_exists = session.execute(email_exists)

        if email_exists.rowcount > 0:
            raise falcon.HTTPBadRequest(
                'Email is registered',
                'User with email: {0} is already registered'.format(email)
            )

        create_user = self.db.Users(
            roles_id = 2,
            username = username,
            email = email,
            password = password,
            location = location
        )

        session.add(create_user)
        session.commit()

        resp.status = falcon.HTTP_201

    def on_get(self):
        pass

server = falcon.API()

user = routes.User(database)
server.add_route('/users/{user}/', user)
