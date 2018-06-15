from datetime import datetime


class RssFeed:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)

        if not self.id:
            self.id = datetime.now().strftime('%y%m%d%H%M%S')

    def __repr__(self):
        return self.__str__()

    def as_dict(self):
        return {'type': 'RssFeed'}


class TwitterFeed(RssFeed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.handle = kwargs.get('handle', '')
        self.last_tweet_id = kwargs.get('last_tweet_id', '')

    def __str__(self):
        return 'TwitterFeed:[h={}, lid={}, id={}]'.format(self.handle,
                                                          self.last_tweet_id,
                                                          self.id)

    def as_dict(self):
        attrs = self.__dict__.copy()
        return attrs.update({'type': 'TwitterFeed'})


class TwitchFeed(RssFeed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.channel_id = kwargs.get('channel_id', None)
        self.last_stream_id = kwargs.get('last_stream_id', '')
        self.title = kwargs.get('title', '')
        self.user_id = kwargs.get('user_id', '')
        self.last_time = kwargs.get('last_time', datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))

    def __str__(self):
        return 'TwitchFeed:[chid={}, lid={}, ti={}, uid={}, id={}]'.format(self.channel_id,
                                                                           self.last_stream_id,
                                                                           self.title,
                                                                           self.user_id,
                                                                           self.id)

    def as_dict(self):
        attrs = self.__dict__.copy()
        return attrs.update({'type': 'TwitchFeed'})


class YouTubeFeed(RssFeed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.channel_id = kwargs.get('channel_id', '')
        self.title = kwargs.get('title', '')
        self.last_video_id = kwargs.get('last_video_id', '')
        self.last_time = kwargs.get('last_time', datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))

    def __str__(self):
        return 'YouTubeFeed:[chid={}, ti={}, lid={}, id={}]'.format(self.channel_id,
                                                                    self.title,
                                                                    self.last_video_id,
                                                                    self.id)

    def as_dict(self):
        attrs = self.__dict__.copy()
        return attrs.update({'type': 'YouTubeFeed'})
