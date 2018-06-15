from servercore import SubdomainHandler
from server.util import *
from server.exceptions import *
from . import eight_ball


class BOTHandler(SubdomainHandler):

    def handle_GET(self):
        if not self.t_path.queries:
            raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Please provide query parameters')

        if self.t_path.topdir == 'eb':
            file = eight_ball.process(self.t_path)
            self.send_response(HTTPStatus.OK)
            self.send_headers(file)
            self.set_file(file)
