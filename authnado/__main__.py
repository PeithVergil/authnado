from tornado.web import Application
from tornado.ioloop import IOLoop

from .config import settings
from .handlers import http


def main():
    loop = IOLoop.current()
    app = Application(http.routes, **settings)
    app.listen(8080)
    loop.start()


if __name__ == '__main__':
    main()
