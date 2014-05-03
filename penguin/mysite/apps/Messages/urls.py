from django.conf.urls import patterns, include, url
from .api_routes import message, sentMessage, receivedMessage 
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^api/message$', message),
	url(r'^api/message/sent$', sentMessage),
	url(r'^api/message/received$', receivedMessage),
)
