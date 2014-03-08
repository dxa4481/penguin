from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('mysite.apps.Users.urls')),
	url(r'^', include('mysite.apps.Tools.urls')),
	url(r'^', include('mysite.apps.Browse.urls')),
)
