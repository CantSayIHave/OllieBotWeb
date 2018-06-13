"""
Registry for www subdomain

Contains allowed directories and file mappings
"""
from server.util import *

allowed_directories = ['html', 'css', 'images']

mappings = {'commands': 'html/commands.html',
            'about': 'html/about.html',
            'status': 'html/status.html',
            'contact': 'html/contact.html',
            'index': 'html/index.html',
            'favicon.ico': 'images/icon.png',
            '': 'html/index.html'}


def allowed(dir):
    return dir in allowed_directories


def map(trans_path: TranslatedPath):
    if trans_path.path in mappings:
        trans_path.update(mappings[trans_path.path])
