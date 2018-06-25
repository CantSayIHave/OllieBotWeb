import twitter as twitterapi
import apis.youtubeapi
import apis.twitchapi
from apis.api_keys import *

twitter = twitterapi.Api(consumer_key=TWITTER_CONSUMER_KEY,
                         consumer_secret=TWITTER_CONSUMER_SECRET,
                         access_token_key=TWITTER_TOKEN_KEY,
                         access_token_secret=TWITTER_TOKEN_SECRET)

youtube = youtubeapi.YoutubeAPI(key=YOUTUBE_TOKEN)

twitch = twitchapi.TwitchAPI(client_id=TWITCH_CLIENT_ID,
                             client_secret=TWITCH_CLIENT_SECRET,
                             oauth=TWITCH_TOKEN)
