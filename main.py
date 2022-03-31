import os
#http://docs.tweepy.org/en/latest/streaming_how_to.html
#https://developer.twitter.com/en/docs/api-reference-index
import tweepy
import dataset
#import creds from the file
import creds
import json

consumer_key = os.environ['Api key']
consumer_secret = os.environ['Api key secret']
access_token = os.environ['Access Token']
access_token_secret = os.environ['Access Token Secret']

db = dataset.connect("sqlite:///minecraft_tweets.db")


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

'''
description = status.user.description
loc = status.user.location
coords = status.coordinates
name = status.user.screen_name
user_created = status.user.created_at
followers = status.user.followers_count
id_str = status.id_str
created = status.created_at
retweets = status.retweet_count
bg_color = status.user.profile_background_color
'''
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):

        #print(f'Location: {status.user.location} followers: {status.user.followers} ')
        #print(f'location: {status.user.location}')
        print(f'screen name: {status.user.screen_name}')

        '''
        print(status.text)
        print(status.user.description)
        print(status.user.location)
        print(status.user.screen_name)
        print(status.coordinates)
        print(status.user.created_at)
        print(status.user.followers_count)
        print('color',status.user.profile_background_color)
        '''
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color

        if coords is not None:
            coords = json.dumps(coords)

        table = db["tweets"]
        table.insert(dict(
            user_name=name,
            user_description=description,
            user_location=loc,
            coordinates=coords,
            text=text,
            user_created=user_created,
            user_followers=followers,
            id_str=id_str,
            created=created,
            retweet_count=retweets,
            user_bg_color=bg_color,))
        print('ding')

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["#keystone"], is_async=True)