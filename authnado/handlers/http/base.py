import json
import logging
from tornado.web import RequestHandler


logger = logging.getLogger(__name__)


class BaseHandler(RequestHandler):

    def initialize(self, executor=None, ioloop=None):
        self.executor = executor
        self.ioloop = ioloop

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def write_error(self, status, **kwargs):
        info = kwargs.get('exc_info')
        if info is None:
            return

        error = info[1]
        reason = getattr(error, 'reason', None)
        if reason is None:
            return

        data = dict(
            status=status,
            error=reason,
        )
        logger.error(data)
        self.jsonify(data)

    def jsonify(self, data):
        self.write(json.dumps(data))
