#!/usr/bin/python
# -*- coding: utf-8 -*-


import TwitterAPI
from TwitterAPI import TwitterAPI
import sys
import sqlite3 as lite
import time
import config_US as config


class TwitterSearch():
    """ Respond to search events and record results to DB"""
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def start_search(self):
        """ Runs the search against the API, parses the result, and persists
            the data to a local SQLlite DB
        """

        PRODUCT = 'fullarchive'
        LABEL = 'test'

        api = TwitterAPI('bGXd4hMWbwbIL0sbiCr32VFt1', '7upMOGqHaxXsKkcJmzQ99Pnsl8nN2IJSi8pFb2PRindtAvhqcg',
                         '4745468882-0Ze9SxSRuQ5bRM72q4xaTL9GmmVMcOHDKq2OLKo',
                         '0KXD22JITm6hk58cowLz3s7qUgBH0JgwfqslBobojH7A9')

        # Check if the API connection is successful
        if not api:
            raise Exception("\n Twitter API connection failed. Check user configuration file.")

        response = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL),
                               {
                                   'query': "place_country: US (\"bear\" OR \"blackbear\" OR \"blackbears\" OR \"ursid\" OR \"ursus\" OR \"ursids\") -football -fans -\"Metz Bear Home\" -\"Bear and Peacock\" -@bearandpeacock -leather -\"Golden Bear\" -drinking -team -Chicago -game -sports -score -polar -soldier -teddy -arms -baseball -inning -innings -JV -halftime -coach -playoffs -varsity -championship -NFL -is:retweet",
                                   'fromDate': '201801010000', 'toDate': '201801050000', "maxResults": 500})
        tweet_count = 0
        for tweet_data in response:
            self.process_tweet(tweet_data)
            tweet_count += 1

        return tweet_count

    def process_tweet(self, data):
        """ Parses individual fields out of a single tweet's JSON, and
            persists the data to the DB
        """

        tweetID = int(data['id_str'])
        # Test data being converted from JSON to mapped fields
        print("tweetID: " + str(tweetID))

        tweetDate = data['created_at']
        user = data['user']['screen_name']
        user_id = data['user']['id_str']
        user_desc = data['user']['description']

        try:
            user_loc = data['user']['location']
        except:
             user_loc = ''

        user_verified = data['user']['verified']

        try:
            user_url = data['entities']['urls'][0]['expanded_url']
        except:
            user_url = ''

        try:
            user_followers = data['user']['followers_count']
        except:
            user_followers = ''

        try:
            user_listed = data['user']['listed_count']
        except:
            user_listed = ''

        try:
            user_statuses = data['user']['statuses_count']
        except:
            user_statuses = ''

        try:
            user_friends = data['user']['friends_count']
        except:
            user_friends = ''

        try:
            user_lang = data['user']['lang']
        except:
            user_lang = ''

        try:
            user_fav = data['user']['favourites_count']
        except:
            user_fav = ''

        try:
            user_geo = data['user']['geo_enabled']
        except:
            user_geo = ''

        try:
            tweet_lat = data['coordinates']['coordinates', ''][1]
        except:
            tweet_lat = 0

        try:
            tweet_long = data['coordinates']['coordinates', ''][0]
        except:
            tweet_long = 0

        try:
            tweetText = data['text']
        except:
            tweetText = ''

        # External URL link embedded in the tweet text itself

        try:
            links = data['entities']['urls'][0]['expanded_url']
        except:
            links = ''
        try:
            linked_photo = data['quoted_status']['entities']['media', []][0]['media_url']
        except:
            linked_photo = ''

        # URL to the embedded photo in THIS tweet (not a linked tweet)

        try:
            media_url = data['entities'].get('media', [])[0]['media_url']
        except:
            media_url = ''

        try:
            hashtags = data['entities']['hashtags', []][0]['text']
        except:
            hashtags = ''

        try:
            tweet_location = data['place']['full_name']
        except:
            tweet_location = ''

        # retrieved data into the SQLite database
        try:
            conn = lite.connect(self.db_filename)
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
            print("\t# Error processing tweet to DB")
            print()
            e
        return

## main script ###

def main(argv):
    db_filename = config.preferences['db_filename']

    search = TwitterSearch(db_filename)

    tweet_count = search.start_search()

    print("Downloaded {0} tweets".format(tweet_count))

if __name__ == "__main__":
    main(sys.argv)