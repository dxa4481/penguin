from django.conf.urls import patterns, url

from .views import browse_tools


urlpatterns = patterns('',
	url(r'^$', browse_tools)
)
