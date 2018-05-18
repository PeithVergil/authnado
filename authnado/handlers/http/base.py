import json
import logging
from datetime import datetime
from tornado.web import RequestHandler


logger = logging.getLogger(__name__)


class BaseHandler(RequestHandler):

    def get_template_namespace(self):
        """
        Pass additional variables to the templates.
        """
        data = super().get_template_namespace()
        data['now'] = datetime.now()
        return data

    def get_current_user(self):
        cookie = self.get_secure_cookie('user')
        if cookie:
            return json.loads(cookie)
        return None

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
        self.write(data)
