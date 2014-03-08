from django.conf.urls import patterns, url
from .views import user_tools, new_tool, tool_editor

urlpatterns = patterns('',
	url(r'^user/tools/$', user_tools, name='user_tools'),
	url(r'^user/tools/new/$', new_tool),
	url(r'^user/tools/edit/$', tool_editor),
)


