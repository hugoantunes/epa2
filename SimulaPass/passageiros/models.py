# -*- coding: utf-8 -*-
from django.db import models
import threading

class Passageiro(models.Model, threading.Thread):
    nome =  models.CharField(max_length=90)
    tem_carro =  models.BooleanField()
    conforto_toleravel = models.IntegerField()
    
    def __unicode__(self):
        return self.nome