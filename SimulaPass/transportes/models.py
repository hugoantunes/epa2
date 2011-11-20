# -*- coding: utf-8 -*-
import threading

from django.db import models

from mundo.models import Quadrante, Simulacao

class Transporte(models.Model, threading.Thread):
    nome =  models.CharField(max_length=90)
    velocidade_confortavel = models.FloatField()
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

    @classmethod
    def todos(cls):
        return Transporte.objects.all().exclude(nome='carro')

class AgenteTransporte(models.Model, threading.Thread):
    tipo_transporte = models.ForeignKey(Transporte, related_name='agente_transporte')
    origem = models.ForeignKey(Quadrante, related_name='origem_transporte', blank=True, null=True)
    destino = models.ForeignKey(Quadrante, related_name='destino_transporte', blank=True, null=True)
    simulacao = models.ForeignKey(Simulacao, related_name='transportes')
    desconforto = models.IntegerField()
    tempo_percurso = models.IntegerField(blank=True, null=True) 
    capacidade_atual = models.IntegerField() 
    
    def __unicode__(self):
        return 'AgenteTransporte: %s-%d' % (self.tipo_transporte.nome,self.id)

    @property
    def ha_vagas(self):
        if self.capacidade_atual < self.tipo_transporte.capacidade_maxima:
            return True
        return False
   
    def passageiro_entrando(self):
        self.capacidade_atual += 1
        self.verifica_conforto()
        self.save()

    def verifica_conforto(self):
        if self.capacidade_atual > self.tipo_transporte.capacidade_confortavel:
            desconforto = self.calcula_desconforto()
            self.desconforto = desconforto

    def calcula_desconforto(self):
        try:
            max_pessoas_desconfortaveis = self.tipo_transporte.capacidade_maxima - self.tipo_transporte.capacidade_confortavel 
            qtd_pessoas_desconfortaveis = self.capacidade_atual - self.tipo_transporte.capacidade_confortavel 
            percent_desconforto = 100*float(qtd_pessoas_desconfortaveis)/float(max_pessoas_desconfortaveis)
        except:
            import ipdb; ipdb.set_trace()
            
        return percent_desconforto
    
    @property
    def status(self):
        if self.capacidade_atual == self.tipo_transporte.capacidade_maxima:
            return 'cheio'
        elif self.capacidade_atual >= self.tipo_transporte.capacidade_maxima/2:
            return 'moderado'
        else:
            return 'vazio'

