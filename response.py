# response module by CantSayIHave
# created 2018/3/14
#
# response class from outgoing responses


import http
import zlib


class Response:
    def __init__(self, status: str = http.OK):
        self.status = status
        self.params = {}
        self.file_bytes = None

    def __bytes__(self):
        return self.read()

    def content_type(self, c_type: str = http.HTML):
        self.params['Content-Type'] = c_type
        return self

    def set_file(self, file_path: str):
        with open(file_path, 'rb') as o:
            self.file_bytes = o.read()
        return self

    def set_file_raw(self, raw_bytes):
        self.file_bytes = raw_bytes
        return self

    def content_length(self, length: int):
        self.params['Content-Length'] = length
        return self

    def add_content_length(self):
        if self.file_bytes:
            self.params['Content-Length'] = len(self.file_bytes)
        return self

    def encoding(self, enc: str):
        if not self.file_bytes:
            raise FileNotFoundError('Response needs a file to add encoding')

        self.params['Content-Encoding'] = enc
        if enc == http.DEFLATE:
            self.file_bytes = zlib.compress(self.file_bytes)
        return self

    def set_json(self, json: str):
        self.params['Content-Type'] = http.JSON
        self.file_bytes = bytes(json, 'utf-8')
        return self

    def set_filename(self, name):
        self.params['Content-Disposition'] = 'inline; filename="{}"'.format(name)
        return self

    def read(self):
        header = 'HTTP/1.1 {}\n'.format(self.status)

        for p_name, p_value in self.params.items():
            header += '{}: {}\n'.format(p_name, p_value)

        header += '\n'

        out = bytes(header, 'utf-8')

        if self.file_bytes:
            out += self.file_bytes

        return out

