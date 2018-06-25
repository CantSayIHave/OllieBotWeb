import io
import json
import shutil

import youtube_dl

import subdomains.util as util
from server.util import *
from server.exceptions import *
from . import eight_ball
from . import registry


class BOTHandler(util.SubdomainHandler):

    def handle_GET(self):
        if not self.t_path.queries:
            raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Please provide query parameters')

        if not registry.allowed(self.t_path.topdir):
            raise HTTPException(HTTPStatus.NOT_FOUND, explain='This endpoint does not exist')

        args = self.t_path.queries

        if self.t_path.topdir == 'eb':
            file = eight_ball.process(self.t_path)
            self.send_response(HTTPStatus.OK)
            self.send_headers(file)
            self.set_file(file)

        elif self.t_path.topdir == 'ytdl':
            if 'key' not in args:
                raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Please supply a key')

            if args['key'] != registry.YTDL_KEY:
                raise HTTPException(HTTPStatus.FORBIDDEN, explain='Key is invalid')

            if 'id' not in args:
                raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Please supply video id')

            url = args['id']

            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]}

            def download_procedure(url, ydl_opts):
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url)
                        return ydl.prepare_filename(info)

                except Exception as e:
                    raise HTTPException(HTTPStatus.NOT_FOUND, explain='Error in video conversion')

            filename = download_procedure(url, options)
            filename = filename.replace('.webm', '')

            new_filename = filename.rsplit('-', 1)[0].replace('_', ' ') + '.mp3'  # clean up name
            old_filename = filename + '.mp3'

            try:
                open(old_filename, 'r').close()
                shutil.move(old_filename, 'resources/audio/{}'.format(new_filename))
                self.send_json({'fn': new_filename}, 'downloaded.json')
            except:
                raise HTTPException(HTTPStatus.NOT_FOUND, explain='Error in video conversion')

    def send_json(self, data, filename: str):
        f = io.BytesIO()
        f.write(bytes(json.dumps(data), 'utf-8'))

        file = File(f, name=filename)
        self.send_response(HTTPStatus.OK)
        self.send_headers(file)
        self.set_file(file)
