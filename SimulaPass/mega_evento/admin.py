# -*- coding:utf-8 -*-

from django.contrib import admin
from mega_evento.models import MegaEvento

class MegaEventoAdmin(admin.ModelAdmin):
    model = MegaEvento

    list_display = ['nome', 'localizacao', 'qtd_pessoas_esperadas']
    search_fields = ['nome']

admin.site.register(MegaEvento, MegaEventoAdmin)
