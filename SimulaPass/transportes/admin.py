# encoding: utf-8

from transportes.models import PerfilTransporte
from django.contrib import admin

class TransporteAdmin(admin.ModelAdmin):
	list_display = ('nome','velocidade_confortavel','capacidade_confortavel','capacidade_maxima')
	list_filter = ['capacidade_confortavel']
	search_fields = ['nome']
	
admin.site.register(PerfilTransporte, TransporteAdmin)
