# -*- coding: utf-8 -*-
from django.db import models

class Mundo(models.Model):
    qtd_pessoas = models.IntegerField(max_length=255)
    qtd_transportes = models.IntegerField(max_length=255)
    qtd_carros = models.IntegerField(max_length=255)
    permite_carros = models.BooleanField()  

class Quadrante(models.Model):
    mundo = models.ForeignKey(Mundo, related_name='quadrantes')
    percentual_pessoas = models.IntegerField(max_length=255)
    percentual_transportes = models.IntegerField(max_length=255)
    permite_carros = models.BooleanField()

    def __unicode__(self):
        return 'quadrante%d_mundo%d'%(self.id, self.mundo.id)

    @property
    def passageiros_do_quadrante(self):
        return int(float(self.mundo.qtd_pessoas)*float(self.percentual_pessoas)/100)
'''    
    @property
    def porcentagem_atual_de_passageiros(self):
        return int(float(self.capacidade_atual)/float(self.capacidade_maxima)*100)
    
    @property
    def porcentagem_maxima_confortavel(self):
        percentual = int(float(self.capacidade_confortavel)/float(self.capacidade_maxima)*100)
        return percentual*2 
'''
