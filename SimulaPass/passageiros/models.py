# -*- coding: utf-8 -*-
import threading

from django.db import models

from transportes.models import AgenteTransporte
from mundo.models import Simulacao, Quadrante

class Passageiro(models.Model):
    nome =  models.CharField(max_length=90)
    tem_carro =  models.BooleanField()
    conforto_toleravel = models.IntegerField()
    
    def __unicode__(self):
        return self.nome

class AgentePassageiro(models.Model, threading.Thread):
    tipo_passageiro = models.ForeignKey(Passageiro, related_name='agente_passageiro')
    transporte = models.ForeignKey(AgenteTransporte, related_name='passageiros', blank=True, null=True)
    tem_carro = models.BooleanField()
    conforto_atual = models.IntegerField() #matar esse campo
    simulacao = models.ForeignKey(Simulacao, related_name='passageiros')
    origem = models.ForeignKey(Quadrante, related_name='origem_passageiro', blank=True, null=True)
    destino = models.ForeignKey(Quadrante, related_name='destino_passageiro', blank=True, null=True)
    
    def __unicode__(self):
        return 'AgentePassageiro: %s-%d' % (self.tipo_passageiro.nome,self.id)
