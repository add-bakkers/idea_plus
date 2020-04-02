# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.http import HttpResponse
from pyknp import Juman
import tweepy
import csv
import seaborn as sns
sns.set(style="whitegrid")
import pandas as pd
import re
import MeCab
from . import make_csv as mc
import codecs
from numpy import mean
import oseti
from . import word_search as ws
from . import jum_analize as jua
import sqlite3
# MeCabインスタンス作成
m = MeCab.Tagger('')
# osetiインスタンス作成
analyzer = oseti.Analyzer()


@login_required
def top_page(request):
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    #全ツイート取得
    mc.mk_twcsv(request)
    #csv読み込み
    with codecs.open('all_tweets.csv', 'r', 'utf-8', 'ignore') as file:
        tw_df = pd.read_csv(file)
    #改行を除く
    text_list = list(tw_df['tweet_text'])
    for i in range(len(text_list)):
        text_list[i] = text_list[i].replace('\n', ' ')
        
    #ここからここからトピック辞書作成
    topic_dict={}
    topic_value={}
    
    conn = sqlite3.connect("wnjpn.db")
    #概念の抽出
    cur = conn.execute("select synset1,synset2 from synlink where link='hypo'")
    #全部纏めた辞書の作成
    word_net_dict = {}
    for row in cur:
        b = row[0]
        n = row[1]
        if n not in word_net_dict:
            word_net_dict[n] = b
    count=0
    for tw in text_list:
        #形態素解析
        twlis = jua.juman_analize(tw)
        #ネガポジ判定
        pnmean = analyzer.analyze(tw)
        flag=False
        for n in twlis:
            n_dict = ws.Search(n.midasi,word_net_dict,conn)
            if len(n_dict)==0:
                imi_dict={}
                for i in n.imis.split():
                    if ':' in i:
                        a=i.split(':')
                        imi_dict[a[0]]=a[1]
                if 'ドメイン' in imi_dict:
                    if ';' in imi_dict['ドメイン']:
                        domain_lis=imi_dict['ドメイン'].split(';')
                        for i in domain_lis:
                            i=i.split('・')
                            i=i[0]
                            n_dict = ws.Search(i,word_net_dict,conn)
                            
                            for id in n_dict:
                                if id in topic_dict:
                                    if pnmean[0]<0:
                                        topic_value[id]=topic_value[id]-1
                                    else:
                                        topic_value[id]=topic_value[id]+1
                                else:
                                    topic_dict[id]=n_dict[id]
                                    topic_value[id]=1
                    else:
                        i=imi_dict['ドメイン']
                        i=i.split('・')
                        i=i[0]
                        n_dict = ws.Search(i,word_net_dict,conn)
                        for id in n_dict:
                            if id in topic_dict:
                                if pnmean[0]<0:
                                    topic_value[id]=topic_value[id]-1
                                else:
                                    topic_value[id]=topic_value[id]+1
                            else:
                                topic_dict[id]=n_dict[id]
                                topic_value[id]=1
            
            for id in n_dict:
                if id in topic_dict:
                    if pnmean[0]<0:
                        topic_value[id]=topic_value[id]-1
                    else:
                        topic_value[id]=topic_value[id]+1
                else:
                    topic_dict[id]=n_dict[id]
                    topic_value[id]=1
    print(topic_value)
    print(count)
    return render(request,'user_auth/top.html',{'user': user})
