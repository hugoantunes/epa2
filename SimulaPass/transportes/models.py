# -*- coding: utf-8 -*-
from django.db import models
import threading

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
        percentual = int(float(self.capacidade_atual)/float(self.capacidade_maxima)*100)
        return percentual
    
    @property
    def porcentagem_maxima_confortavel(self):
        percentual = int(float(self.capacidade_confortavel)/float(self.capacidade_maxima)*100)
        target = percentual*2
        return target
