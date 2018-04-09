from . import base


class Hello(base.BaseHandler):

    def get(self):
        self.jsonify(dict(text='Hello, World!'))


class AddUser(base.BaseHandler):

    def post(self):
        self.set_status(201)
        self.jsonify(dict(
            id=54321,
            name='Hello World',
            address='Sample Address',
        ))


class GetUser(base.BaseHandler):

    def get(self, user_id):
        self.jsonify(dict(
            id=user_id,
            name='Hello World',
            address='Sample Address',
        ))

    def put(self, user_id):
        self.jsonify(dict(
            id=user_id,
            name='Hello World',
            address='Sample Address',
        ))
