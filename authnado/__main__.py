import logging
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

    loop = IOLoop.current()
    app = Application(http.routes, **settings)
    app.listen(8080)
    loop.start()


if __name__ == '__main__':
    main()
