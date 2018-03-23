from globals import *
from bot import eight_ball
import http


class SubdomainBOT:
    def __init__(self, request, socket):
        self.request = request
        self.socket = socket

    def handle(self):
        q = self.request.query  # type: str
        try:
            args = extract_args(q)
        except ValueError:
            raise http.BadRequestError('Please provide arguments.')
        except Exception:
            raise http.BadRequestError('Incorrect argument formatting.')

        if q.startswith('eb') or q.startswith('eight_ball'):
            resp = eight_ball.process(args)

            self.socket.send(resp.read())

