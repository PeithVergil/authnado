import logging
from concurrent import futures
from tornado.web import Application
from tornado.ioloop import IOLoop

from .config import settings
from .handlers import http


def logs():
    if settings.get('debug'):
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level)


def main():
    logs()

    with futures.ThreadPoolExecutor(settings.get('THREAD_COUNT')) as executor:
        loop = IOLoop.current()
        params = dict(
            ioloop=loop,
            executor=executor,
        )
        app = Application(http.routes(params), **settings)
        app.listen(settings.get('PORT'))
        loop.start()


if __name__ == '__main__':
    main()
