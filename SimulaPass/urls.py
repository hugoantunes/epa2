import settings

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),

    
    url(r'^simulacao/$', 'SimulaPass.views.home', name='home'),
	url(r'^ajax/(?P<numero>\d+)/$', 'SimulaPass.views.ajax'),

	url(r'^teste/$', 'SimulaPass.views.teste'),
	
	url(r'^posiciona_passageiros/(?P<numero>\d+)/$', 'SimulaPass.views.posiciona_passageiro'),
	url(r'^posiciona_transportes/(?P<numero>\d+)/$', 'SimulaPass.views.posiciona_transporte'),
    
    url(r'^mundo/(?P<id_mundo>\d+)/passageiro/transporte/quadrante/(?P<id_quadrante>\d+)/$','SimulaPass.views.entra_no_transporte'),
	
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root':settings.MEDIA_ROOT}
    ),
)
