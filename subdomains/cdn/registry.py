"""
Registry for cdn

Contains allowed directories, endpoint mappings
"""

allowed_endpoints = ['eb', 'ytdl']

endpoint_mappings = {'eb': 'eight_ball_im'}


def allowed(dir):
    return dir in allowed_endpoints
