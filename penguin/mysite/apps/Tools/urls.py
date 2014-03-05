from django.conf.urls import patterns, url
from mysite.apps.Tools import views

urlpatterns = patterns('',
	url(r'^$', views.user_tools, name='user_tools')
)
