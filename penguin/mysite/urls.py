from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    (r'^$', include('mysite.apps.Users.urls')),
    (r'^register/$', include('mysite.apps.Users.urls')),
)
