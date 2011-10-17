# -*- coding: utf-8 -*-
import threading

from django.db import models

from mundo.models import Quadrante, Simulacao

class Transporte(models.Model, threading.Thread):
    nome =  models.CharField(max_length=90)
    tempo_viagem = models.FloatField()
    capacidade_maxima = models.IntegerField()
    capacidade_atual = models.IntegerField()
    capacidade_confortavel = models.IntegerField()
    
    def __unicode__(self):
        return self.nome

    @property
    def porcentagem_atual_de_passageiros(self):
        return int(float(self.capacidade_atual)/float(self.capacidade_maxima)*100)
    
    @property
    def porcentagem_maxima_confortavel(self):
        percentual = int(float(self.capacidade_confortavel)/float(self.capacidade_maxima)*100)
        return percentual*2

class AgenteTransporte(models.Model, threading.Thread):
    tipo_transporte = models.ForeignKey(Transporte, related_name='quadrantes_origens')
    origem = models.ForeignKey(Quadrante, related_name='quadrantes_origens', blank=True, null=True)
    destino = models.ForeignKey(Quadrante, related_name='quadrantes_destinos', blank=True, null=True)
    simulacao = models.ForeignKey(Simulacao, related_name='transportes')
    desconforto = models.IntegerField()
    capacidade_atual = models.IntegerField() 
    
    def __unicode__(self):
        return 'AgenteTransporte: %s-%d' % (self.tipo_transporte.nome,self.id)
     
