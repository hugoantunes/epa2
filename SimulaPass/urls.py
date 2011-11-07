#encoding: utf-8

import settings

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
    
    url(r'^simulacao/$', 'SimulaPass.views.home', name='home'),
	url(r'^ajax/(?P<numero>\d+)/$', 'SimulaPass.views.ajax'),

    #tela da simulação
    url(r'^teste/$', 'SimulaPass.views.index'),
    #cria simulação e agentes da simulação
    url(r'^constroi_mundo/(?P<id_mundo>\d+)/$','SimulaPass.views.constroi_mundo'),
    #dado um passageiro ele entra em um transporte
    url(r'^aloca_passageiro/(?P<id_passageiro>\d+)/$','SimulaPass.views.aloca_passageiros'),
    
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root':settings.MEDIA_ROOT}
    ),
)
