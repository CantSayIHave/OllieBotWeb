import http
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus
import shutil
import mimetypes
import io

from server.util import *
from server.exceptions import *
import server
from subdomains import www, bot, cdn


class ServerCoreHandler(BaseHTTPRequestHandler):
    server_version = "OllieBotWeb/" + http.server.__version__

    __commands__ = ['do_GET', 'do_POST']

    def __getattribute__(self, item: str):  # assumes `item` is a do_{} styled string
        """Adds and tries any command to allow subdomain routing

        (yes, perhaps this the wrong way to do it)"""

        if item.startswith('do_'):
            if item not in self.__commands__:
                self.__commands__.append(item)

                def new_com():
                    self.do(item.split('_', 1)[1].replace(' ', ''))  # do() the command

                self.__setattr__(item, new_com)
                return new_com
            else:
                return super().__getattribute__(item)
        else:
            return super().__getattribute__(item)

    def do_GET(self):
        self.do('GET')

    def do_POST(self):
        self.do('POST')

    def do(self, command):
        """A workaround to add subdomain routing at the server level"""

        if 'Host' in self.headers:
            host = self.headers['Host']
        else:
            host = 'www.{}'.format(server.domain_name)  # assume www

        subdomain = host.split(server.domain_name)[0].replace('.', '')  # extract subdomain, assuming www

        handler = None

        if subdomain == 'www' or subdomain == '':
            handler = www.get_handler()
        elif subdomain == 'bot':
            handler = bot.get_handler()
        elif subdomain == 'cdn':
            handler = cdn.get_handler()

        if handler:
            if not handler.has_command(command):
                self.send_error(HTTPStatus.NOT_IMPLEMENTED,
                                message='This subdomain does not support command {}'.format(command))
                return

            command_func = handler.command(command)

            try:
                command_func()
            except HTTPException as e:
                self.send_error(e.status, message=e.message, explain=e.explain)
            except Exception as e:
                self.send_error(HTTPStatus.BAD_REQUEST,
                                message='Bad Request - Unknown exception',
                                explain='Exception: {}'.format(e))
        else:
            self.send_error(HTTPStatus.NOT_FOUND, message='Not Found')


class SubdomainHandler:
    def __init__(self, handler: ServerCoreHandler):
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


def execute(server_class, server_handler):
    server_address = '', 80
    core_server = server_class(server_address, server_handler)
    core_server.serve_forever()


try:
    execute(HTTPServer, ServerCoreHandler)
except Exception as e:
    print('Critical Exception: {}\n'
          'Shutting down...'
          ''.format(e))
