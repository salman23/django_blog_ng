from django.conf.urls import patterns, include, url
import views
from django.views.generic import ListView
from views import PostListView
from models import Post

urlpatterns =  patterns(
        '',
        # Index
        url('^$', ListView.as_view(
        model=Post,
        paginate_by = 5,
        )),

    )