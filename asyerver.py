import asyncore
import socket
from subdomains.core import get_subdomain_handler
from request import Request
from globals import *
from response import Response
import http


class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        if data:
            raw = data.decode('utf-8')
            print(raw)

            request = Request(raw)

            sd_handler = get_subdomain_handler(request, self)

            try:
                sd_handler.handle()
            except Exception as e:
                if hasattr(e, 'code'):
                    status_code = e.code
                else:
                    status_code = http.NOT_FOUND

                if hasattr(e, 'message'):
                    message = e.message
                else:
                    message = '404 - Not Found'

                resp = Response(status=status_code)\
                    .content_type(http.HTML)\
                    .set_file_raw(bytes('<html><body><h1>{}</h1> Error: {}</body></html>\n'.format(message, e),
                                        'utf-8'))

                self.send(resp.read())

        self.close()


class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = EchoHandler(sock)


server = EchoServer('', 80)
try:
    asyncore.loop()
except KeyboardInterrupt:
    server.close()
