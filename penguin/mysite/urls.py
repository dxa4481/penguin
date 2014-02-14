from django.conf.urls import patterns, include, url
from mysite.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^userEditor/$', userEditor),
    url(r'^$', login),
    url(r'^loggedIn/$', loggedIn),
)
