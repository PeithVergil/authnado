from functools import partial
from tornado.web import Application
from tornado.ioloop import IOLoop


from .auth import AuthnadoProvider
from .config import settings
from .handlers import http


class App(Application):

    def __init__(self, pool, loop=None):
        if loop is None:
            loop = IOLoop.current()
        executor = partial(loop.run_in_executor, pool)
        provider = AuthnadoProvider(executor)
        super().__init__(http.routes(
            executor=executor,
            provider=provider,
        ), **settings)
