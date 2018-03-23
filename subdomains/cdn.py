from globals import *
import http
from response import Response


class SubdomainCDN:
    def __init__(self, request, socket):
        self.request = request
        self.socket = socket

    def handle(self):
        q = self.request.query  # type: str
        try:
            args = extract_args(q)
        except ValueError:
            args = None

        perm = False
        if args and 'k' in args:
            perm = check_content_key(args['k'])

        # structure: eb/eb_img.png?k={key}
        if q.startswith('eb') and args:
            if not perm:
                raise http.ForbiddenError('Key invalid.')

            filepath = q.split('?')[0].replace('eb', 'eight_ball_im', 1)
            filename = filepath.split('/')[1]

            resp = Response().content_type(http.PNG).set_filename(filename).set_file(filepath)

            self.socket.send(resp.read())

