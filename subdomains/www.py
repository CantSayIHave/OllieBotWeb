from mappings import *
import response
import http
from globals import *


class SubdomainWWW:
    def __init__(self, request, socket):
        self.request = request
        self.socket = socket

    def handle(self):

        if any([x in self.request.query for x in ['html', 'css', 'image', 'ico']]):
            q = self.request.query
        else:
            q = menu_mapping[self.request.query]  # type: str
        # q = self.request.query

        # send default html file
        if not q:

            resp = response.Response().content_type(http.HTML).set_file(DEFAULT_HTML)

            self.socket.send(resp.read())

        # access directory css/ for each file
        elif q.startswith('css'):
            resp = response.Response().content_type(http.CSS).set_file(q)

            self.socket.send(resp.read())

        elif q.startswith('html'):
            resp = response.Response().content_type(http.HTML).set_file(q)

            self.socket.send(resp.read())

        elif q.startswith('images'):
            if q.endswith('png'):
                resp_type = http.PNG
            elif q.endswith('jpg'):
                resp_type = http.JPG
            else:
                raise(ValueError('bad file type request'))

            resp = response.Response().content_type(resp_type).set_file(q)

            self.socket.send(resp.read())

        elif q == 'favicon.ico':
            resp = response.Response().content_type(http.PNG).set_file('favicon.png')

            self.socket.send(resp.read())

        else:
            raise(http.NotFoundError('bad request'))