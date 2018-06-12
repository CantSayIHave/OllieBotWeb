from http import HTTPStatus


class HTTPException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        status = args[0]
        self.status = status
        self.code = status.value
        self.message = status.phrase

    def __str__(self):
        return '{} - {}'.format(self.code, self.message)
