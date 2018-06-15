import os

from servercore import SubdomainHandler
from server.util import *
from server.exceptions import *
from . import registry


class WWWHandler(SubdomainHandler):

    def handle_GET(self):
        self.map_path()
        self.check_errors()

        self.send_response(HTTPStatus.OK)
        self.send_headers(self.t_path.file)
        self.set_file(self.t_path.file)

    def map_path(self):
        """Maps the requested path and adds '.html' extension if necessary (default guess)"""

        registry.map(self.t_path)

        if not self.t_path.resource.endswith(('.html', '.css', '.jpg', '.png', '.ico')):  # default to html
            self.t_path += '.html'

    def check_errors(self):
        """Checks for errors with security or file existence"""

        if not self.t_path.topdir in registry.allowed_directories:
            raise HTTPException(HTTPStatus.FORBIDDEN)

        if not self.t_path.exists():
            raise HTTPException(HTTPStatus.NOT_FOUND)
