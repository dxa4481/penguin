from django.conf.urls import patterns, include, url
from .api_routes import borrowTransaction, getToolsBorrowing, getToolsLending
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
		url(r'^api/borrowTransaction/$', borrowTransaction),
		url(r'^api/borrowTransaction/borrowing/(?P<user_id>\w{0,50})/$', getToolsBorrowing),
		url(r'^api/borrowTransaction/borrowed/(?P<user_id>\w{0,50})/$', getToolsLending),

)
