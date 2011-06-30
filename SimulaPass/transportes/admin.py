# encoding: utf-8

from transportes.models import Transporte
from django.contrib import admin

class TransporteAdmin(admin.ModelAdmin):
	list_display = ('nome','tempo_viagem','coeficiente_conforto','capacidade_maxima')
	list_filter = ['coeficiente_conforto']
	search_fields = ['nome']
	
admin.site.register(Transporte, TransporteAdmin)