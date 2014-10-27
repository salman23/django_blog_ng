from django.conf.urls import patterns, include, url
import views
from django.views.generic import ListView
from models import Post

urlpatterns =  patterns(
        '',
        # Index
        url(r'^$', ListView.as_view(model=Post,)),
    ) 