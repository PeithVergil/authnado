import logging
from concurrent import futures
# from tornado.web import Application
from tornado.ioloop import IOLoop

from .app import App
from .config import settings
# from .handlers import http


def logs():
    if settings.get('debug'):
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level)


def main():
    logs()

    with futures.ThreadPoolExecutor(settings.get('thread_size')) as executor:
        loop = IOLoop.current()
        app = App(executor, loop)
        app.listen(settings.get('port'))
        loop.start()


if __name__ == '__main__':
    main()
