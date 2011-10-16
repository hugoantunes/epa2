# -*- coding: utf-8 -*-

from django.db import models
from mundo.models import Quadrante

class MegaEvento(models.Model):
    nome = models.CharField(max_length=255)
    localizacao = models.ForeignKey(Quadrante,related_name='evento')
    qtd_pessoas_esperadas = models.IntegerField(max_length=255)

    def __unicode__(self):
        return self.nome
