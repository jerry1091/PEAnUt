#!/usr/bin/env python

from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from core import create_app


app = create_app()


class MainHandler(RequestHandler):
    def get(self):
        self.write("This message comes from Tornado ^_^")


tr = WSGIContainer(app)

application = Application([
    (r"/tornado", MainHandler),
    (r".*", FallbackHandler, dict(fallback=tr)),
])

if __name__ == "__main__":
    application.listen(18080, address='0.0.0.0')
    IOLoop.instance().start()
