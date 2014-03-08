from django.conf.urls import patterns, url
from .views import user_tools, new_tool, tool_editor

urlpatterns = patterns('',
	url(r'^$', user_tools, name='user_tools'),
	url(r'^new/$', new_tool),               
	url(r'^edit/$', tool_editor)
)
