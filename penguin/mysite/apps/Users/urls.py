from django.conf.urls import patterns, include, url
from .api_routes import userById, user, login, changePassword, logout, get_admins
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'mysite.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^api/user/(?P<user_id>\w{0,50})$', userById),
	url(r'^api/user$', user),
	url(r'^api/login$', login),
	url(r'^api/changePassword', changePassword),
	url(r'^api/logout', logout),
	url(r'^api/admins', get_admins),
	#url(r'^api/get_user_tools', get_user_tools),
	#url(r'^user/edit/$', user_editor),

)

