from functools import partial
from tornado.web import Application
from tornado.ioloop import IOLoop

from .config import settings
from .handlers import http


class App(Application):

    def __init__(self, executor, loop=None):
        if loop is None:
            loop = IOLoop.current()
        self.run = partial(loop.run_in_executor, executor)
        super().__init__(http.routes, **settings)
