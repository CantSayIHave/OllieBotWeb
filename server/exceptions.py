from http import HTTPStatus


class HTTPException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        if args:
            status = args[0]
        else:
            status = kwargs.get('status', HTTPStatus.NOT_FOUND)

        self.status = status
        self.code = status.value
        self.message = status.phrase
        self.explain = kwargs.get('explain', None)

    def __str__(self):
        return '{} - {}'.format(self.code, self.message)
