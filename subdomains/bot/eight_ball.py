
from globals import *
from server.exceptions import *
from server.util import *
from http import HTTPStatus
import http
import random
import os
import io
import json


def process(t_path: TranslatedPath) -> File:
    args = t_path.queries
    if 'token' not in args:
        raise HTTPException(HTTPStatus.FORBIDDEN, explain='Token not found')

    if not valid_token(args['token']):
        raise HTTPException(HTTPStatus.FORBIDDEN, explain='Token invalid.')

    img = args.get('img', None)

    if not img:
        img = random.choice(os.listdir("eight_ball_im"))

    url = 'http://cdn.olliebot.cc/eb/{}?k={}'.format(img, get_content_key())

    file = io.BytesIO()
    json.dump({'url': url}, file)

    return File(file, name='selection.json')

