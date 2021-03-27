import tweepy
import time
import random
import configparser
import schedule

conf = configparser.ConfigParser()
conf.read('config.ini')

CONSUMER_KEY = conf['twitter']['API_KEY']
CONSUMER_SECRET = conf['twitter']['API_SECRET']
ACCESS_TOKEN = conf['twitter']['ACCESS_TOKEN']
ACCESS_SECERET = conf['twitter']['ACCESS_TOKEN_SECRET']


# consumer　第一引数に(consumer　key)　第二引数に(consumer　secret) #
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
# ACCESS_TOKEN_KEY 第一引数に(Access token)　第二引数に(Access token secret) #
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECERET)

# wait_on_rate_limit = レート制限が補充されるのを自動的に待つかどうか #
# wait_on_rate_limit_notify = Tweepyがレート制限の補充を待っているときに通知を出力するかどうか #
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# screen name (@name)を取得
my_name = api.me()
my_screen_name = my_name.screen_name


# 取得したいキーワード #
list = ['大学　だるい','大学　めんど','当選　したい','当選　お願いします','稼ぎたい','バイト　行かなきゃ',
                'バイト　行きたくない','バイト　めんどくさい','仕事　辞めたい','免許証　写真','リモート　今日','暇　バイト']

reserve = ['大学　だるい','大学　めんど','当選　したい','当選　お願いします','稼ぎたい','バイト　行かなきゃ',
                'バイト　行きたくない','バイト　めんどくさい','仕事　辞めたい','免許証　写真','リモート　今日','暇　バイト']
# ツイート数10件 #
tweet_count = 100

#自動フォローと判定されにくいようにフォロー間隔 sleep をダンダム値とする
random_min_time = 4 #sleepでとり得る最小値
random_max_time = 15 #sleepでとり得る最大値


def main():
    # for search in search_list:
    global list
    global reserve
    if list == 0:
        list = reserve
    search_list = random.choice(list)
    search = search_list
    liked_count = 0 #いいねカウンター

    print(my_screen_name,': ','------------------------------')
    print(my_screen_name,': ','Searching... {}' .format(search))
    # サーチ結果を格納
    search_result = api.search(q=search, count=tweet_count)

    for tweet in search_result:
        tweet_id = tweet.id
        user_name = tweet.user._json['name']
        user_screen_name = tweet.user._json['screen_name']
        tweet_status = api.get_status(tweet_id)
        tweet_favorite_status = tweet_status.favorited

        check_status = 'False'
        tweet_favorite_status_01 = str(tweet_favorite_status)


        if tweet_favorite_status_01 == check_status:
            if liked_count == 12:
                continue
            try:
                api.create_favorite(id=tweet_id)   # いいねの処理
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                continue
            tweet_status = api.get_status(tweet_id)
            tweet_favorite_status = tweet_status.favorited
            print(my_screen_name,': ',user_name,'(',user_screen_name,")","いいねしました(STATUS =",tweet_favorite_status,")")
            liked_count += 1
            sleep_random_time = random.randint(random_min_time,random_max_time)
            print(my_screen_name,': ',' 次のいいねまで' ,sleep_random_time,'秒待ちます')
            time.sleep(sleep_random_time)
        else:
            print(my_screen_name,': ',user_name,'(',user_screen_name,')','はいいね済み(',tweet_favorite_status,')なのでスキップしました')

    print(my_screen_name,": ","search =",search,"で",liked_count,"人いいねしました。終了します。")
    list.remove(search)


schedule.every(2).hours.do(main)


while True:
  schedule.run_pending()
  time.sleep(60)
