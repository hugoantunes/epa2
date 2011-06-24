# -*- coding: utf-8 -*-

from passageiros.models import Passageiro
from django.contrib import admin

class PassageiroAdmin(admin.ModelAdmin):
	list_display = ('nome','tem_carro','conforto_toleravel')
	list_filter = ['tem_carro']
	search_fields = ['nome']
	
admin.site.register(Passageiro, PassageiroAdmin)