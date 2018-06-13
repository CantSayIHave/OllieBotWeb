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
        self.send_headers()
        self.set_file(self.translated.file)

    def map_path(self):
        """Maps the requested path and adds '.html' extension if necessary"""

        registry.map(self.translated)

        if not self.translated.resource.endswith(('.html', '.css', '.jpg', '.png', '.ico')):  # default to html
            self.translated += '.html'

    def check_errors(self):
        """Checks for errors with security or file existence"""

        if not self.translated.topdir in registry.allowed_directories:
            raise HTTPException(HTTPStatus.FORBIDDEN)

        if not self.translated.exists():
            raise HTTPException(HTTPStatus.NOT_FOUND)

    def send_headers(self):
        """Adds appropriate headers based on file"""

        content_type = self.extensions_map['.' + self.translated.filetype]
        file_stat = os.fstat(self.translated.file.fileno())
        file_size = file_stat.st_size
        file_time = file_stat.st_mtime

        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', file_size)
        self.send_header("Last-Modified", self.date_time_string(file_time))
        self.end_headers()
