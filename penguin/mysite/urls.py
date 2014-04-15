from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('mysite.apps.Users.urls')),
	url(r'^', include('mysite.apps.Tools.urls')),
	url(r'^', include('mysite.apps.Browse.urls')),
	url(r'^$', 'django.contrib.staticfiles.views.serve', kwargs={
		'path': 'index.html'}),
)
print(settings.STATICFILES_DIRS)
