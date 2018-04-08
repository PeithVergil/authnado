from . import base


class Hello(base.BaseHandler):

    def get(self):
        self.jsonify(dict(text='Hello, World!'))
