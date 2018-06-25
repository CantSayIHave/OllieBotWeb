import shutil
import mimetypes
from http.server import BaseHTTPRequestHandler

from server.util import *


class SubdomainHandler:
    def __init__(self, handler: BaseHTTPRequestHandler):  # really a ServerCoreHandler
        self.handler = handler
        self.t_path = TranslatedPath(handler.path)

        self.send_response = handler.send_response
        self.send_header = handler.send_header
        self.end_headers = handler.end_headers
        self.date_time_string = handler.date_time_string

    def has_command(self, command: str):
        return hasattr(self, 'handle_{}'.format(command))

    def command(self, _command):
        return getattr(self, 'handle_{}'.format(_command), None)

    def __getitem__(self, item):
        return self.command(item)

    def set_file(self, f):
        if isinstance(f, str):
            f = open(f, 'rb')
        elif isinstance(f, File):
            f = f.get()
        shutil.copyfileobj(f, self.handler.wfile)

    def get_file(self):
        f = io.BytesIO()
        shutil.copyfileobj(self.handler.rfile, f)
        return f

    def send_headers(self, file: File):
        """Adds appropriate headers based on file"""

        content_type = self.extensions_map['.' + file.type]

        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', file.size)
        self.send_header('Last-Modified', self.date_time_string(file.time))
        self.send_header('Content-Disposition', 'inline; filename="{}"'.format(file.name))
        self.end_headers()

    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'text/html',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        '.json': 'text/json'
    })
