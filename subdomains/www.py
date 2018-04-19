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
        elif self.request.query in menu_mapping:
            q = menu_mapping[self.request.query]  # type: str
        else:
            q = self.request.query
        # q = self.request.query
        if 'discordapp' in self.request.raw:
            raise http.NotFoundError('Not Found.')
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

            resp = response.Response().content_type(resp_type).set_file(q).chunked()

            out_bytes = bytes(resp)

            sent = self.socket.write_chunked(resp)
            print('\nlength of out_bytes:{}\nlength of sent:{}'.format(len(out_bytes), sent))

        elif q == 'favicon.ico':
            resp = response.Response().content_type(http.PNG).set_file('favicon.png')

            self.socket.send(resp.read())

        elif q.startswith('google'):
            resp = response\
                .Response()\
                .content_type(http.HTML)\
                .set_filename('google25abf33f5985d2fc.html')\
                .set_file('google25abf33f5985d2fc.html')

            self.socket.send(resp.read())

        elif q.startswith('think'):  # it would make you think, in fact
            resp = response.Response(status=http.FOUND).set_location('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

            self.socket.send(bytes(resp))

        else:
            raise(http.NotFoundError('bad request'))