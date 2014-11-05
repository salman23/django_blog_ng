from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', views.home, name='home' ),
    # url(r'^$', 'django_blog_ng_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Admin urls
    url(r'^admin/', include(admin.site.urls)),
    # Blog urls
    url(r'', include('blogengine.urls')),
    # FlatPages url
    url(r'', include('django.contrib.flatpages.urls')),
)
