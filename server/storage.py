import json
from .containers import *
from globals import *

make_file_safe('resources/rss.json')


def load_rss() -> list:
    with open('resources/rss.json', 'r') as f:
        feeds = json.load(f)
        formatted_feeds = []
        for feed in feeds:
            _type = feed['type']
            if _type == 'TwitterFeed':
                formatted_feeds.append(TwitterFeed(**feed))
            elif _type == 'TwitchFeed':
                formatted_feeds.append(TwitchFeed(**feed))
            elif _type == 'YouTubeFeed':
                formatted_feeds.append(YouTubeFeed(**feed))

        return formatted_feeds


def save_rss(feeds: list):
    """
    :type feeds: list[RssFeed]
    """
    with open('resource/rss.json', 'w') as f:
        json.dump([x.__dict__ for x in feeds], f)
