# Twitch API wrapper for getting channels and scraping streams
# **Sync version
# Created by CantSayIHave, 8/19/2017, Updated 6/17/2018
# Open source

import requests


class TwitchAPI:
    v5_api = 'application/vnd.twitchtv.v5+json'

    def __init__(self, client_id: str, client_secret: str, oauth: str = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = oauth

        self.initialize()

    def initialize(self):
        if not self.oauth_token:
            self.oauth_token = self.get_new_token()
        else:
            auth = self.check_auth()
            if not auth:
                self.oauth_token = self.get_new_token()

    def get_new_token(self):
        p = requests.post('https://api.twitch.tv/kraken/oauth2/token'
                          '?client_id={}'
                          '&client_secret={}'
                          '&grant_type=client_credentials'
                          ''.format(self.client_id, self.client_secret))  # type: requests.Response

        if p.status_code == 200:
            auth = p.json()
            return auth['access_token']
        else:
            raise ValueError('Auth request failed')

    def check_auth(self):
        r = requests.get('https://api.twitch.tv/kraken', headers=self.build_header())

        if r.status_code == 200:
            auth = r.json()
            return auth['token']['valid']
        else:
            raise ValueError('TwitchAPI: Auth check failed, HTTP code {}'.format(r.status_code))

    def build_header(self):
        h = {'Accept': self.v5_api,
             'Client-ID': self.client_id,
             'Authorization': 'OAuth {0}'.format(self.oauth_token)}
        return h

    def get_channel_from_name(self, name: str):
        self.get_auth()
        r = requests.get('https://api.twitch.tv/kraken/users?login={0}'.format(name),
                        headers=self.build_header())

        if r.status_code == 200:
            channel = r.json()
            if channel['_total'] == 1:
                return channel['users'][0]
            return None
        else:
            raise ValueError('Channel request failed')

    def get_channel(self, _id: str):
        self.get_auth()
        r = requests.get('https://api.twitch.tv/kraken/channels/{0}'.format(_id),
                        headers=self.build_header())

        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            return None
        else:
            raise ValueError('Channel request failed')

    def get_stream(self, channel_id: str):
        self.get_auth()
        r = requests.get('https://api.twitch.tv/kraken/streams/{0}'.format(channel_id),
                        headers=self.build_header())

        if r.status_code == 200:
            stream = r.json()
            if stream['stream']:
                return stream
            return None
        else:
            raise ValueError('Stream request failed')

    def get_auth(self):
        auth = self.check_auth()
        if not auth:
            self.oauth_token = self.get_new_token()
