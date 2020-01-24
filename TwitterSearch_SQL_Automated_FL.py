#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import time
import TwitterSearch_config_FL as config
import tweepy
import json

global tweetCount
tweetCount = 0


class TwitterSearch():
    """ Respond to search events and record results to DB"""

    def __init__(self):
        # Call the search
        self.start_search()

    def start_search(self):
        # Read the user access keys to access API
        auth = tweepy.OAuthHandler(config.keys['consumer_key'], config.keys['consumer_secret'])
        auth.set_access_token(config.keys['access_token'], config.keys['access_secret'])

        # Initialize API
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        # Check if the API connection is successful
        if not api:
            print "\n Twitter API connection failed. Check user configuration file."

        # print("Downloading max {0} tweets".format(maxTweets))

        try:
            searchQuery = config.searchQuery
            for tweet in tweepy.Cursor(api.search, q=searchQuery, count=tweetsPerQuery, lang="en", result_type="recent",
                                       include_entities=True).items(maxTweets):
                # print tweet.id
                self.process_tweet(tweet)
                global tweetCount
                tweetCount += 1

        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
        return

    def process_tweet(self, data):
        tweetID = int(data.id_str)
        # Test data being converted from JSON to mapped fields
        print "tweetID: " + str(tweetID)
        tweetDate = data.created_at
        user = data.user.screen_name
        user_id = data.user.id_str
        user_desc = data.user.description.encode('utf-8')
        user_loc = data.user.location.encode('utf-8') if not None else ''
        user_verified = data.user.verified
        if 'urls' in data.user.entities:
            user_url = data.user.entities.get('urls', [])[0]['expanded_url'].encode('utf-8') if not None else ''
        else:
            user_url = ''
        user_followers = data.user.followers_count if not None else 0
        user_listed = data.user.listed_count if not None else 0
        user_statuses = data.user.statuses_count
        user_friends = data.user.friends_count if not None else 0
        user_lang = data.user.lang if not None else ''
        user_fav = data.user.favourites_count if not None else 0
        user_geo = data.user.geo_enabled if not None else ''
        try:
            tweet_lat = data.coordinates.get('coordinates', '')[1]
        except:
            tweet_lat = 0

        try:
            tweet_long = data.coordinates.get('coordinates', '')[0]
        except:
            tweet_long = 0
        tweetText = data.text.encode('utf-8') if not None else ''
        # External URL link embedded in the tweet text itself
        try:
            links = data.entities.get('urls')[0]['expanded_url'] if not None else ''
        except:
            links = ''
        try:
            linked_photo = data.quoted_status.entities.get('media', [])[0]['media_url'] if not None else ''
        except:
            linked_photo = ''

        # URL to the embedded photo in THIS tweet (not a linked tweet)
        try:
            media_url = data.entities.get('media', [])[0]['media_url'] if not None else ''
        except:
            media_url = ''
        try:
            hashtags = data.entities.get('hashtags', [])[0]['text'] if not None else ''
        except:
            hashtags = ''
        tweet_location = data.place.full_name if not None else ''

        # retrieved data into the SQLite database
        try:
            conn = lite.connect(db_filename)
            conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
            cursor = conn.cursor()

            cursor.execute('''INSERT into tweets (tweetID, tweetDate, user, user_id, user_desc, user_loc, user_verified, user_url, \
            user_followers, user_listed, user_statuses, user_friends, user_lang, user_fav, user_geo, \
            tweet_lat, tweet_long, tweetText, links, linked_photo, media_url, hashtags, tweet_location) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (tweetID, tweetDate, user, user_id, user_desc, user_loc, user_verified, user_url, \
                            user_followers, user_listed, user_statuses, user_friends, user_lang, user_fav, user_geo, \
                            tweet_lat, tweet_long, tweetText, links, linked_photo, media_url, hashtags, tweet_location))
            # save change to db and log progress
            conn.commit()
            conn.close()
        except Exception as e:
            print "\t# Error processing tweet to DB"
            print e
        return


## main script ###

def main(argv):
    global db_filename
    db_filename = config.preferences['db_filename']
    global maxTweets
    maxTweets = config.preferences['maxTweets']
    global tweetsPerQuery
    tweetsPerQuery = config.preferences['tweetsPerQuery']
    global searchQuery
    searchQuery = config.searchQuery

    search = TwitterSearch()
    search.start_search()


if __name__ == "__main__":
    main(sys.argv)

# Finally
print("Downloaded {0} tweets".format(tweetCount))