from django.conf.urls import patterns, include, url
import views
from django.views.generic import ListView, DetailView
from views import PostListView
from models import Post

urlpatterns =  patterns(
        '',
        # Index
        url(r'^$', ListView.as_view(
        model=Post,
        paginate_by = 5,
        )),
        url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<pub_date__day>\d{1,2})/(?P<slug>[\w-]+)/$',
            DetailView.as_view(
                model = Post,
            ),
        ),
    )