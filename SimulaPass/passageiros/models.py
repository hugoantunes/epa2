# -*- coding: utf-8 -*-
import threading

from django.db import models

from transportes.models import AgenteTransporte, PerfilTransporte
from mundo.models import Simulacao, Quadrante

class PerfilPassageiro(models.Model):
    nome =  models.CharField(max_length=90)
    tem_carro =  models.BooleanField()
    conforto_toleravel = models.IntegerField()
    
    def __unicode__(self):
        return self.nome

class AgentePassageiro(models.Model, threading.Thread):
    tipo_passageiro = models.ForeignKey(PerfilPassageiro, related_name='agente_passageiro')
    transporte = models.ForeignKey(AgenteTransporte, related_name='passageiros', blank=True, null=True)
    tem_carro = models.BooleanField()
    conforto_atual = models.IntegerField() #matar esse campo
    simulacao = models.ForeignKey(Simulacao, related_name='passageiros')
    origem = models.ForeignKey(Quadrante, related_name='origem_passageiro', blank=True, null=True)
    destino = models.ForeignKey(Quadrante, related_name='destino_passageiro', blank=True, null=True)
    
    def __unicode__(self):
        return 'AgentePassageiro: %s-%d' % (self.tipo_passageiro.nome,self.id)
    
    @property
    def dentro_transporte(self):
        if self.transporte:
            return True
        return False

    def entra_carro(self):
        tipo_carro = PerfilTransporte.objects.get(nome='carro')
        carro = AgenteTransporte.objects.create(
            tipo_transporte = tipo_carro,
            simulacao=self.simulacao,
            origem=self.origem, 
            destino=self.destino,  
            capacidade_atual=1,
            desconforto=0,
        )
        self.transporte = carro
        self.tem_carro = True
        self.save()

    def entra_transporte(self, transporte):
        self.transporte = transporte 
        transporte.passageiro_entrando()
        self.avalia_conforto()
        self.save()

    def avalia_conforto(self):
        self.conforto_atual -= self.transporte.desconforto
