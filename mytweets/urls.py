from django.conf.urls import patterns, include, url
from django.contrib import admin
from tweets import views
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mytweets.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.Index.as_view()),
    # url(r'^$', views.Index.get),
    url(r'^user/(\w+)/$', views.Profile.as_view(), name='user'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/(\w+)/post/$', views.PostTweet.as_view()),
    url(r'^hashTag/(\w+)/$', views.HashTagCloud.as_view()),
    url(r'^search/$', views.Search.as_view(), name='search'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^profile/$',views.UserRedirect.as_view()),
    url(r'^mostFollowed/$', views.MostFollowedUsers.as_view()),
)


