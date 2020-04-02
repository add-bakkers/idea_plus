import django.contrib.auth.views
from django.urls import path,include
from . import views
from django.conf.urls import url
from . import poker_headsup_main
app_name='poker'

urlpatterns=[
    path('play/',poker_headsup_main.main, name="play"),
    path('top/',views.top_page, name="top"),
]
