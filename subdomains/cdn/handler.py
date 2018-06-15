from servercore import SubdomainHandler
from server.util import *
from server.exceptions import *
from globals import *
from . import registry


class CDNHandler(SubdomainHandler):

    def handle_GET(self):
        if not registry.allowed(self.t_path.topdir):
            raise HTTPException(HTTPStatus.NOT_FOUND, explain='No endpoint "{}" exists'.format(self.t_path.topdir))

        args = self.t_path.queries
        key_perm = False

        if args and 'k' in args:
            key_perm = check_content_key(args['k'])

        if self.t_path.topdir == 'eb':
            self.check_key(args, key_perm)

            self.t_path.replace('eb', 'eight_ball_im')
            self.check_file()
            self.send_headers(self.t_path.file)
            self.set_file(self.t_path.file)

    @staticmethod
    def check_key(args, key_perm):
        if not args:
            raise HTTPException(HTTPStatus.FORBIDDEN, explain='Please provide a content key')

        if not key_perm:
            raise HTTPException(HTTPStatus.FORBIDDEN, explain='Content key invalid.')

    def check_file(self):
        if not self.t_path.exists():
            raise HTTPException(HTTPStatus.NOT_FOUND, explain='No file "{}" was found.'.format(self.t_path.resource))

    def send_headers(self, file: File):
        """Adds appropriate headers based on file"""

        content_type = self.extensions_map['.' + file.type]

        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', file.size)
        self.send_header('Last-Modified', self.date_time_string(file.time))
        self.send_header('Content-Disposition', 'inline; filename="{}"'.format(file.name))
        self.end_headers()
