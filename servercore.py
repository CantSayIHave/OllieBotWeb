import http
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

from server.util import *
from server.exceptions import *
import server
from subdomains import www, bot, cdn, rss


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

        handler_class = None

        if subdomain == 'www' or subdomain == '':
            handler_class = www.get_handler()
        elif subdomain == 'bot':
            handler_class = bot.get_handler()
        elif subdomain == 'cdn':
            handler_class = cdn.get_handler()
        elif subdomain == 'rss':
            handler_class = rss.get_handler()

        if handler_class:
            handler = handler_class(self)
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


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def execute(server_class, server_handler):
    server_address = '', 80
    core_server = server_class(server_address, server_handler)
    core_server.serve_forever()


try:
    rss.handler.begin_scraping()
    execute(ThreadedHTTPServer, ServerCoreHandler)
except Exception as e:
    print('Critical Exception: {}\n'
          'Shutting down...'
          ''.format(e))
    rss.handler.stop_scraping()
