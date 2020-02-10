######################################################
##One-time database creation
import sqlite3

conn = sqlite3.connect('C:\\Users\\akell\\OneDrive - Colostate\\PhD\\Ch4_Twitter\\Data\\Bears_Fl_noReplies.db')
c = conn.cursor()
c.execute('''CREATE TABLE tweets
    (tweetID integer primary key,
    tweetDate datetime,
    user text,
    user_id text,
    user_desc text,
    user_loc text,
    user_verified text,
    user_url text,
    user_followers integer,
    user_listed integer,
    user_statuses integer,
    user_friends integer,
    user_lang text,
    user_fav integer,
    user_geo text,
    tweet_lat real,
    tweet_long real,
    tweetText text,
    links text,
    linked_photo text,
    media_url text,
    hashtags text,
    tweet_location text
    )''')
conn.commit()
conn.close()

##End one-time database creation
######################################################