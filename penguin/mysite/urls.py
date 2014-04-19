from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


urlpatterns = patterns('',
	url(r'^', include('mysite.apps.Users.urls')),
	url(r'^', include('mysite.apps.Tools.urls')),
	url(r'^', include('mysite.apps.Browse.urls')),
	url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
	url(r'^$', 'django.contrib.staticfiles.views.serve', kwargs={
		'path': 'index.html'}),
)
print(settings.STATICFILES_DIRS)
