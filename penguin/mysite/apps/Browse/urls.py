from django.conf.urls import patterns, url

from .views import browse_tools, borrow_tool


urlpatterns = patterns('',
	url(r'^browse/$', browse_tools),
	url(r'^browse/borrow/$', borrow_tool),
)

