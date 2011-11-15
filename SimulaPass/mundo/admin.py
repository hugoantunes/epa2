# -*- coding: utf-8 -*-

from django.contrib import admin
from mundo.models import Mundo, Quadrante, DistanciasQuadrante

class MundoAdmin(admin.ModelAdmin):
    model = Mundo

    list_display = ['id','qtd_pessoas','qtd_transportes','permite_carros']
    list_filter = ['permite_carros']
    search_fields = ['id']

class QuadranteAdmin(admin.ModelAdmin):
    model = Quadrante

    list_display = ['id','percentual_pessoas', 'percentual_transportes', 'permite_carros', 'vazao_confortavel', 'vazao_maxima']
    list_filter = ['permite_carros']
    search_fields = ['id']

class DistanciasQuadranteAdmin(admin.ModelAdmin):
    model = DistanciasQuadrante

    list_display = ['__str__', 'distancia']

admin.site.register(Mundo, MundoAdmin)
admin.site.register(Quadrante, QuadranteAdmin)
admin.site.register(DistanciasQuadrante, DistanciasQuadranteAdmin)
