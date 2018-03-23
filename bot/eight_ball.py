from response import Response
from globals import *
import http
import random
import os
import json


def process(args: dict) -> Response:
    if 'token' not in args:
        raise http.ForbiddenError('Token not found.')

    if not valid_token(args['token']):
        raise http.ForbiddenError('Token invalid.')

    img = args.get('img', None)

    if not img:
        img = random.choice(os.listdir("eight_ball_im"))

    url = 'http://cdn.olliebot.cc/eb/{}?k={}'.format(img, get_content_key())

    return Response().set_json(json.dumps({'url': url}))

