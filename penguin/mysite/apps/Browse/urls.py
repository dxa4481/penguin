from django.conf.urls import patterns, include, url
from .api_routes import borrowTransaction
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
		url(r'^api/borrowTransaction/$', borrowTransaction),

)
