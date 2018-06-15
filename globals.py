# globals module by CantSayIHave
# created 2018/3/10
#
# global functions, classes, and constants


# pulls a tag from http request
# assumes delimiters are space ' ' and newline '\n'


import urllib.parse as urllib
import ast
from api_keys import *
from base64 import b64encode
import os


def http_pull_tag(tag: str, request: str, dl1=' ', dl2='\n') -> str:
    tag_start = request.find(tag)
    if tag_start > -1:
        tag_start = request.find(dl1, tag_start) + 1
        return request[tag_start:request.find(dl2, tag_start)]
    else:
        return ''


def response_prefix(status: str, type: str) -> bytes:
    out = 'HTTP/1.1 {}\n' \
          'Content-Type: {}\n' \
          '\n'.format(status, type)
    return bytes(out, 'utf-8')


def is_num(sample):
    try:
        ast.literal_eval(sample)
        return True
    except Exception:
        return False


def extract_args(request: str) -> dict:
    if '?' not in request:
        raise ValueError('Missing ? separator')  # yes this is petty

    decoded = urllib.unquote(request.split('?')[1])

    return {k: map_primitive(v) for k, v in [x.split('=') for x in decoded.split('&')]}  # unhelpful comment


def map_primitive(text: str):
    lower = text.lower()
    if lower == 'true':
        return True
    elif lower == 'false':
        return False
    elif lower == 'none':
        return None
    elif is_num(lower):
        return ast.literal_eval(lower)
    else:
        return text


def make_file_safe(path):
    try:
        open(path, 'r')
    except:
        open(path, 'w').close()


def valid_token(token: str):
    return token in discord_tokens


def generate_token(bits: int):
    return b64encode(os.urandom(bits)).decode('utf-8').replace('/', '').replace('=', '')


CONTENT_KEY = generate_token(8)


def get_content_key():
    global CONTENT_KEY
    return CONTENT_KEY


def check_content_key(key: str):
    global CONTENT_KEY
    return key == CONTENT_KEY


DOMAIN_NAME = 'olliebot.cc'

DEFAULT_HTML = 'index.html'

