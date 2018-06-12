import asyncore
import socket
from http import server

from old_subdomains.core import get_subdomain_handler
from request import Request
from response import Response

RECV_CHUNK = 8192
SEND_CHUNK = 55000

server.BaseHTTPRequestHandler

class SocketHandler(asyncore.dispatcher):
    buffer = b''

    def handle_read(self):
        data = self.recv(RECV_CHUNK)
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

    # def handle_write(self):
    #     data = self.buffer
    #     sent = self.send(data[:SEND_CHUNK])
    #
    #     while sent < len(data):
    #         if sent == 0:
    #             self.handle_close()
    #             return 0
    #         sent = self.send(data[sent:sent + SEND_CHUNK])
    #     return sent

    def write(self, data):
        self.buffer += data

    def writable(self):
        return bool(len(self.buffer))

    def write_chunked(self, resp: Response):
        sent = self.send(resp.read_header())

        if sent == 0:
            self.handle_close()
            return 0

        total_sent = sent
        sent = 0

        while sent < len(resp):
            result = self.send(self.build_chunk(resp.file_bytes[sent:sent + SEND_CHUNK]))
            if result == 0:
                self.handle_close()
                return 0
            sent += SEND_CHUNK

        total_sent += sent

        sent = self.send(self.build_chunk(b''))

        return sent + total_sent

    @staticmethod
    def build_chunk(data):
        size = hex(len(data))[2:]
        return bytes(size, 'utf-8') + b'\r\n' + data + b'\r\n'

    def handle_write(self):
        data = self.buffer
        sent = self.send(data)
        while sent < len(data):
            if sent == 0:
                self.handle_close()
                return 0
            sent = self.send(data[sent:])
        self.flush()

    def flush(self):
        self.buffer = b''


class SocketServer(asyncore.dispatcher):
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
            handler = SocketHandler(sock)


server = SocketServer('', 80)
try:
    asyncore.loop()
except KeyboardInterrupt:
    server.close()
