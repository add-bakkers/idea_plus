from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.http import HttpResponse
import tweepy
import csv
import seaborn as sns
sns.set(style="whitegrid")
import pandas as pd
from . import twitter_api
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl

request_token=[]
def mk_twcsv(request):
    key          = twitter_api.CONSUMER_KEY
    key_secret   = twitter_api.CONSUMER_SECRET_KEY
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    token        = user.access_token['oauth_token']
    token_secret = user.access_token['oauth_token_secret']
    
    # 認証情報
    auth = tweepy.OAuthHandler(key, key_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    
    all_tweets=[]
    
    latest_tweets = api.user_timeline(count=200,tweet_mode="extended")
    all_tweets.extend(latest_tweets)
    
    
     
    while len(latest_tweets)>0:
        latest_tweets = api.user_timeline(count=200, max_id=all_tweets[-1].id-1,tweet_mode="extended")
        all_tweets.extend(latest_tweets)
     
    with open('all_tweets.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['tweet_text'])
        
        for tweet in all_tweets:
            tw=tweet.full_text
            if (tw.startswith('RT')):
                tw=tw[3:]
            writer.writerow([tw])
    pd.read_csv('all_tweets.csv')
