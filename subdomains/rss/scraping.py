import re

from apis import twitter, youtube, twitch
from server.containers import *

"""
Old Method
----------
1. Take bot, server, feed
2. Scrape online feed
3. Send messages based on response and feed history

New Method
----------
1. Take feed
2. Scrape online feed
3. Update feed and return True, or return False
(how I should've done it in the first place)
"""


def scrape_twitter(rss_feed: TwitterFeed):
    twitter_feed = twitter.GetUserTimeline(screen_name=rss_feed.handle, count=1)
    if twitter_feed:
        last_tweet = twitter_feed[0]
        if last_tweet and last_tweet.id != rss_feed.last_tweet_id:
            rss_feed.last_tweet_id = last_tweet.id
            return True

    return False


def scrape_youtube(rss_feed: YouTubeFeed):
    search = None
    try:
        search = youtube.get_channel_videos(rss_feed.channel_id, 1)
    except Exception as e:
        print(e)
    if search:
        last_vid = search[0]
        last_vid_id = str(last_vid['id']['videoId'])
        last_vid_time = last_vid['snippet']['publishedAt']
        if last_vid_id != rss_feed.last_video_id and last_vid_time != rss_feed.last_time:
            rss_feed.last_video_id = last_vid_id
            rss_feed.last_time = last_vid_time
            return True

    return False


def scrape_twitch(rss_feed: TwitchFeed):
    stream = None
    try:
        stream = twitch.get_stream(rss_feed.channel_id)
    except ValueError as e:
        print(e)
    if stream and stream['stream']['_id'] != rss_feed.last_stream_id:
        rss_feed.last_stream_id = stream['stream']['_id']
        return True

    return False

"""
Setup Methods
-------------
Takes necessary info and builds a feed object
"""


def setup_twitter(handle: str) -> TwitterFeed:
    feed = TwitterFeed(handle=handle)
    scrape_twitter(feed)
    return feed


def setup_twitch(username: str) -> TwitchFeed:
    if 'www.twitch.tv/' in username:
        username = username.split('www.twitch.tv/')[1]

    twitch_channel = twitch.get_channel_from_name(username)
    if not twitch_channel:
        raise ValueError('Channel does not exist!')

    feed = TwitchFeed(channel_id=twitch_channel['_id'],
                      title=twitch_channel['display_name'],
                      user_id=username)
    scrape_twitch(feed)
    return feed


def setup_youtube(username: str = None, id: str = None) -> YouTubeFeed:
    youtube_channel = None

    if username:
        youtube_channel = youtube.get_channel_by_name(username)
    elif id:
        youtube_channel = youtube.get_channel_by_id(id)

    if not youtube_channel:
        raise ValueError('Channel does not exist!')

    feed = YouTubeFeed(channel_id=youtube_channel['id'],
                       title=youtube_channel['snippet']['title'])
    scrape_youtube(feed)
    return feed
