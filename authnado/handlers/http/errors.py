from . import base


class Http404(base.BaseHandler):

    def prepare(self, *args, **kwargs):
        self.set_status(404)
