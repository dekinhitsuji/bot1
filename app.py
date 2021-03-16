import tweepy
import configparser
import json
from requests_oauthlib import OAuth1Session
import pandas as pd
import random
import time

conf = configparser.ConfigParser()
conf.read('config.ini')


API_KEY = conf['twitter']['API_KEY']
API_SECRET = conf['twitter']['API_SECRET']
ACCESS_TOKEN = conf['twitter']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = conf['twitter']['ACCESS_TOKEN_SECRET']

twitter = OAuth1Session(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
url = 'https://api.twitter.com/1.1/statuses/update.json'

df = pd.read_csv('test.csv')
text = df['ツイート文']

x = len(df)
list = []
for i in range(x):
    ppp = df.at[i,'ツイート文']

    list.append(ppp)

reserve = []
for i in range(x):
    ddd = df.at[i,'ツイート文']

    reserve.append(ddd)

def main():
    for k in range(x):

        #ツイートをランダムで選択
        tweet = random.choice(list)

        #Twitterにツイートを送信
        params = {'status':tweet}
        response = twitter.post(url, params=params)

        #成功したか否か
        print(response.status_code)

        #使用したものをリストから消去
        list.remove(tweet)


        time.sleep(3600)


main()
