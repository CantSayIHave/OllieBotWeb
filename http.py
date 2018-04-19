# http module by CantSayIHave
# created 2018/3/14
#
# http constants


OK = '200 OK'
FOUND = '302 FOUND'
BAD_REQUEST = '400 BAD REQUEST'
FORBIDDEN = '403 FORBIDDEN'
NOT_FOUND = '404 NOT FOUND'


HTML = 'text/html'
CSS = 'text/css'
JSON = 'text/json'
PNG = 'image/png'
JPG = 'image/jpg'

GZIP = 'gzip'
DEFLATE = 'deflate'


class NotFoundError(Exception):
    code = NOT_FOUND
    message = '404 - Not Found'
    pass


class SubdomainNotFoundError(Exception):
    code = NOT_FOUND
    message = '404 - Not Found'
    pass


class ForbiddenError(Exception):
    code = FORBIDDEN
    message = '403 - Forbidden'
    pass


class BadRequestError(Exception):
    code = BAD_REQUEST
    message = '400 - Bad Request'
    pass

