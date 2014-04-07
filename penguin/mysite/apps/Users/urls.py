from django.conf.urls import patterns, include, url
from .api_routes import user, login
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/user', user),
    url(r'^api/login', login),
    #url(r'^user/edit/$', user_editor),

)

