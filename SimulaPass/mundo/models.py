# -*- coding: utf-8 -*-
from django.db import models

class Mundo(models.Model):
    qtd_pessoas = models.IntegerField(max_length=255)
    qtd_transportes = models.IntegerField(max_length=255)
    qtd_carros = models.IntegerField(max_length=255)
    permite_carros = models.BooleanField()  

    def __unicode__(self):
        return "mundo_%d" %self.id

class Quadrante(models.Model):
    mundo = models.ForeignKey(Mundo, related_name='quadrantes')
    percentual_pessoas = models.IntegerField(max_length=255)
    percentual_transportes = models.IntegerField(max_length=255)
    permite_carros = models.BooleanField()
     
    vazao_confortavel = models.IntegerField(max_length=255)
    vazao_moderada = models.IntegerField(max_length=255)
    vazao_maxima = models.IntegerField(max_length=255)

    def __unicode__(self):
        return 'quadrante%d_mundo%d'%(self.id, self.mundo.id)

    @property
    def passageiros_do_quadrante(self):
        return int(float(self.mundo.qtd_pessoas)*float(self.percentual_pessoas)/100)

class DistanciasQuadrante(models.Model):
    origem = models.ForeignKey(Quadrante, related_name='distancias_origens')
    destino = models.ForeignKey(Quadrante, related_name='distancias_destinos')
    distancia = models.IntegerField(max_length=255) 
    
    def __unicode__(self):
        return 'distancia_q%d_q%d' %(self.origem.id, self.destino.id)

class Simulacao(models.Model):
    mundo = models.ForeignKey(Mundo, related_name='simulacoes')
    qtd_pessoas_usadas = models.IntegerField(max_length=255)
    qtd_transportes_usados = models.IntegerField(max_length=255)
    qtd_carros_usados = models.IntegerField(max_length=255)
    tempo_total = models.IntegerField(max_length=255)
    conforto_total = models.IntegerField(max_length=255)

    def __unicode__(self):
        return 'Simulacao: %d' %self.id
