from django.conf.urls import patterns, include, url
from .views import login, register, user_page, logout
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', login),
    url(r'^register/$', register),
    url(r'^user/$', user_page),
    url(r'^logout/$', logout),
    #url(r'^user/edit/$', user_editor),

)

