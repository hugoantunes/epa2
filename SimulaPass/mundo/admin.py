# -*- coding: utf-8 -*-

from django.contrib import admin
from mundo.models import Mundo, Quadrante, DistanciasQuadante

class QuadranteInline(admin.TabularInline):
    extra = 0
    model = Quadrante

class MundoAdmin(admin.ModelAdmin):
    model = Mundo
    inlines = (QuadranteInline,)

    list_display = ['id','qtd_pessoas','qtd_transportes','permite_carros']
    list_filter = ['permite_carros']
    search_fields = ['id']

class DistanciasQuadrantesAdmin(admin.ModelAdmin):
    model = DistanciasQuadante
   
    list_display = ['__str__','distancia']

admin.site.register(Mundo, MundoAdmin)
admin.site.register(DistanciasQuadante, DistanciasQuadrantesAdmin)
