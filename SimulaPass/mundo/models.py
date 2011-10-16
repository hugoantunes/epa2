# -*- coding: utf-8 -*-
from django.db import models

class Mundo(models.Model):
    qtd_pessoas = models.IntegerField(max_length=255)
    qtd_transportes = models.IntegerField(max_length=255)
    permite_carros = models.BooleanField()    

class Quadrante(models.Model):
    mundo = models.ForeignKey(Mundo, related_name='quadrantes')
    percentual_pessoas = models.IntegerField(max_length=255)
    percentual_transportes = models.IntegerField(max_length=255)
    permite_carros = models.BooleanField()

    def __unicode__(self):
        return 'quadrante%d_mundo%d'%(self.id, self.mundo.id)
