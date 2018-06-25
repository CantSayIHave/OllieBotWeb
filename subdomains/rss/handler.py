import json
import io
import time

import subdomains.util as util
from server.util import *
from server.exceptions import *
from server.containers import *
import server.storage as storage
from globals import *
from . import scraping
import server.scheduler as scheduler


rss_feeds = storage.load_rss()
scraping_delay = 70


def get_feed(id=None, name=None) -> RssFeed:
    if id:
        for feed in rss_feeds:  # type: RssFeed
            if feed.id == id:
                return feed
    elif name:
        for feed in rss_feeds:
            if isinstance(feed, TwitterFeed) and name == feed.handle:
                return feed
            elif isinstance(feed, TwitchFeed) and name == feed.user_id:
                return feed
            elif isinstance(feed, YouTubeFeed) and name == feed.channel_id:
                return feed


class RSSHandler(util.SubdomainHandler):

    def handle_GET(self):
        self.check_token()
        args = self.t_path.queries

        if self.t_path.topdir == 'feeds':
            feed = None
            if 'id' in args:
                feed = get_feed(id=args['id'])
            elif 'name' in args:
                feed = get_feed(name=args['name'])

            if not feed:
                raise HTTPException(HTTPStatus.NOT_FOUND, explain='Feed does not exist')

            f = io.BytesIO()
            f.write(bytes(json.dumps(feed.as_dict()), 'utf-8'))

            file = File(f, name='feed.json')
            self.send_response(HTTPStatus.OK)
            self.send_headers(file)
            self.set_file(file)

    def handle_POST(self):
        self.check_token()
        args = self.t_path.queries

        if self.t_path.topdir == 'feeds':
            if 'type' not in args:
                raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Please specify feed type with `type` argument')
            feed_type = args['type']
            if feed_type == 'twitter':
                if 'handle' not in args:
                    raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Please provide twitter handle')

                handle = args['handle'].replace('@', '', 1)  # remove `@` from handle

                feed = scraping.setup_twitter(handle)

            elif feed_type == 'twitch':
                if 'username' not in args:
                    raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Please provide twitch username')

                feed = scraping.setup_twitch(args['username'])

            elif feed_type == 'youtube':
                if 'username' not in args and 'id' not in args:
                    raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Please provide username or id')

                if 'username' in args:
                    feed = scraping.setup_youtube(username=args['username'])
                else:
                    feed = scraping.setup_youtube(id=args['id'])
            else:
                raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Feed type does not exist!')

            rss_feeds.append(feed)
            storage.save_rss(rss_feeds)

            f = io.BytesIO()
            f.write(bytes(json.dumps(feed.as_dict()), 'utf-8'))

            file = File(f, name='feed.json')
            self.send_response(HTTPStatus.OK)
            self.send_headers(file)
            self.set_file(file)

    def check_token(self):
        if not self.t_path.queries or 'token' not in self.t_path.queries:
            raise HTTPException(HTTPStatus.BAD_REQUEST, explain='Please supply a token.')

        if not valid_token(self.t_path.queries['token']):
            raise HTTPException(HTTPStatus.FORBIDDEN, explain='Token is invalid.')


@scheduler.thread
def scrape_feeds(eq: scheduler.EventQueue):
    while True:
        for feed in rss_feeds:
            if isinstance(feed, TwitterFeed):
                scraping.scrape_twitter(feed)
            elif isinstance(feed, TwitchFeed):
                scraping.scrape_twitch(feed)
            elif isinstance(feed, YouTubeFeed):
                scraping.scrape_youtube(feed)

        try:
            scheduler.sleep(eq, scraping_delay, step_size=2.0)
        except scheduler.TimerException:
            return


def begin_scraping():
    scheduler.start('scrape_feeds')


def stop_scraping():
    scheduler.stop('scrape_feeds')
