# -*- coding: utf-8 -*-
from django.db import models
import threading

class Transporte(models.Model, threading.Thread):
    nome =  models.CharField(max_length=90)
    tempo_viagem = models.FloatField()
    capacidade_maxima = models.IntegerField()
    capacidade_atual = models.IntegerField()
    coeficiente_conforto = models.IntegerField()
    
    def __unicode__(self):
        return self.nome
