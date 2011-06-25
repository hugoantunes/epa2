from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^simulacao/$', 'SimulaPass.views.home', name='home'),
	url(r'^ajax/$', 'SimulaPass.views.ajax', name='home'),
	
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root':settings.MEDIA_ROOT}
    ),
)
